#!/usr/bin/env python3
"""query — the lens over the experiment record (DuckDB view, always fresh).

JSONL indexes + per-run sidecars are the source of truth; this materialises an
in-memory `runs` view joined on `run_id` (the host-agnostic key), so you can ask
cross-run questions weeks later:

    python pace/query.py                       # summary table
    python pace/query.py "gpu='h200' and state='COMPLETED'"
    python pace/query.py "params->>'jps'='10'"           # per-experiment knob (NULL where absent)
    python pace/query.py --dirty                          # runs whose code was uncommitted (repro risk)
    python pace/query.py --sql "SELECT slug, count(*) FROM runs GROUP BY 1"

Heterogeneous experiments coexist: uniform dims are columns; per-experiment knobs
live in `params` and are reached via `params->>'<knob>'`, NULL where they don't apply.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import duckdb
except ImportError:
    print("duckdb not installed (it's a pixi dep): `pixi run python pace/query.py`", file=sys.stderr)
    sys.exit(1)


def _build(repo: Path) -> "duckdb.DuckDBPyConnection":
    con = duckdb.connect()
    subs = repo / "pace" / "submissions.jsonl"
    res = repo / "pace" / "results.jsonl"
    meta_glob = str(repo / "results" / "**" / "job_meta.json")
    rslt_glob = str(repo / "results" / "**" / "job_result.json")

    # Indexes (skip the optional {"_schema":N} sentinel line via filter_pushdown on run_id)
    con.execute(f"""
        CREATE VIEW subs AS
        SELECT * FROM read_json_auto('{subs}', union_by_name=true, format='nd')
        WHERE run_id IS NOT NULL
    """) if subs.exists() else con.execute("CREATE VIEW subs AS SELECT NULL run_id WHERE 1=0")

    if res.exists():
        con.execute(f"""
            CREATE VIEW res AS
            SELECT run_id, state, elapsed, shell_rc
            FROM read_json_auto('{res}', union_by_name=true, format='nd')
            WHERE run_id IS NOT NULL
        """)
    else:
        con.execute("CREATE VIEW res AS SELECT NULL run_id, NULL state, NULL elapsed, NULL shell_rc WHERE 1=0")

    # Sidecars: repro from job_meta, bench from job_result (union_by_name → heterogeneous-safe).
    # Cast nested objects to JSON so `->>` works regardless of which keys a struct has
    # (a GPU-less host gives gpu={present:false} with no `name`; strict struct access would fail).
    try:
        con.execute(f"""
            CREATE VIEW metas AS
            SELECT run_id, to_json(repro) AS repro, to_json(gpu) AS gpu_json
            FROM read_json_auto('{meta_glob}', union_by_name=true)
            WHERE run_id IS NOT NULL
        """)
    except Exception:
        con.execute("CREATE VIEW metas AS SELECT NULL run_id, NULL repro, NULL gpu_json WHERE 1=0")
    try:
        con.execute(f"""
            CREATE VIEW jr AS
            SELECT run_id, bench_summary FROM read_json_auto('{rslt_glob}', union_by_name=true)
            WHERE run_id IS NOT NULL
        """)
    except Exception:
        con.execute("CREATE VIEW jr AS SELECT NULL run_id, NULL bench_summary WHERE 1=0")

    con.execute("""
        CREATE VIEW runs AS
        SELECT s.run_id, s.slug, s.host_kind, s.gpu_tag,
               COALESCE(m.gpu_json->>'name', s.gpu_tag) AS gpu,
               r.state, r.elapsed, r.shell_rc,
               to_json(s.params) AS params, s.question, s.result_dir,
               m.repro, to_json(jr.bench_summary) AS bench_summary
        FROM subs s
        LEFT JOIN res r   USING (run_id)
        LEFT JOIN metas m USING (run_id)
        LEFT JOIN jr      USING (run_id)
    """)
    return con


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("where", nargs="?", help="SQL WHERE clause over the `runs` view")
    ap.add_argument("--sql", help="full SQL query over `runs`")
    ap.add_argument("--dirty", action="store_true", help="runs with uncommitted code (repro risk)")
    ap.add_argument("--repo-root", default=None)
    args = ap.parse_args()

    repo = Path(args.repo_root) if args.repo_root else _git_root()
    con = _build(repo)

    if args.sql:
        q = args.sql
    elif args.dirty:
        q = "SELECT run_id, slug, repro->>'code_sha' sha, repro->>'env_lock' env FROM runs WHERE repro->>'code_dirty'='true'"
    elif args.where:
        q = f"SELECT run_id, slug, gpu, state, elapsed, params, question FROM runs WHERE {args.where}"
    else:
        q = "SELECT run_id, slug, host_kind, gpu, state, elapsed FROM runs ORDER BY run_id"

    try:
        con.execute(q)
        cols = [d[0] for d in con.description]
        rows = con.fetchall()
    except Exception as e:
        print(f"query error: {e}", file=sys.stderr)
        return 2

    print(" | ".join(cols))
    for r in rows:
        print(" | ".join("" if v is None else str(v) for v in r))
    print(f"\n({len(rows)} rows)")
    return 0


def _git_root() -> Path:
    import subprocess
    try:
        return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    except Exception:
        return Path.cwd()


if __name__ == "__main__":
    sys.exit(main())
