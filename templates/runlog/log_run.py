#!/usr/bin/env python3
"""log_run — the dispatcher half of the experiment record (run by /gpu-exp-submission).

Mints the host-agnostic, human-friendly `run_id`, opens the narrative journal stub
(so the *why* is recorded at submit time), and emits `export` lines the sbatch / run
script `eval`s so the machine layer (job_meta.py) stamps the SAME run_id.

    eval "$(python pace/log_run.py --slug prefetch-pilot --machine pace \
              --question 'does prefetch cut prefill?' \
              --params '{"M":2048,"prefetch_depth":3}' --seed 42 \
              --model meta-llama/Llama-3.1-8B-Instruct --model-revision 0e9e39f)"
    # ... now submit; jm_write_meta picks up RUN_ID / JM_* from the env ...

Single-process at submit time → the pretty sequential id never races a fan-out peer.
Import-free of anything heavy; stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

JOURNAL_DIR = "runlog"  # narrative home (NOT experiments/, which is bench code here)


def _repo_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    try:
        top = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        return Path(top)
    except Exception:
        return Path.cwd()


def _next_seq(repo: Path, date: str, machine: str) -> int:
    """Highest existing `r<date>.<machine>.NN` + 1, scanning the submissions index
    and every journal file. Single submit process, so no lock needed."""
    pat = re.compile(rf"r{re.escape(date)}\.{re.escape(machine)}\.(\d+)\b")
    seen: set[int] = set()
    sources = [repo / "pace" / "submissions.jsonl"]
    sources += sorted((repo / JOURNAL_DIR).glob("*.md")) if (repo / JOURNAL_DIR).exists() else []
    for src in sources:
        try:
            for m in pat.finditer(src.read_text(errors="ignore")):
                seen.add(int(m.group(1)))
        except Exception:
            pass
    return (max(seen) + 1) if seen else 1


def _journal_path(repo: Path, slug: str) -> Path:
    month = time.strftime("%Y-%m")
    return repo / JOURNAL_DIR / f"{month}-{slug}.md"


def _ensure_journal(repo: Path, jp: Path, slug: str, question: str | None) -> None:
    jp.parent.mkdir(parents=True, exist_ok=True)
    if jp.exists():
        return
    tpl = repo / JOURNAL_DIR / "_TEMPLATE.md"
    body = tpl.read_text() if tpl.exists() else "# <slug> — <question>\n\n## Runs\n"
    sha = _git_sha(repo)
    body = (body.replace("<slug>", slug)
                .replace("<one-line question>", question or "<question>")
                .replace("<git_sha>", sha)
                .replace("2026-06-13", time.strftime("%Y-%m-%d")))
    jp.write_text(body)
    _index_add(repo, jp, slug, question)


def _git_sha(repo: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], text=True
        ).strip()
    except Exception:
        return "unknown"


def _index_add(repo: Path, jp: Path, slug: str, question: str | None) -> None:
    idx = repo / JOURNAL_DIR / "INDEX.md"
    header = "# Run journals\n\n| campaign | started | question |\n|---|---|---|\n"
    if not idx.exists():
        idx.write_text(header)
    row = f"| [{jp.name}]({jp.name}) | {time.strftime('%Y-%m-%d')} | {question or ''} |\n"
    with idx.open("a") as f:
        f.write(row)


def _append_stub(jp: Path, run_id: str, machine: str, question: str | None,
                 params: dict, seed: int | None, model: str | None) -> None:
    pj = json.dumps(params, ensure_ascii=False) if params else "{}"
    stub = (
        f"\n### {run_id}  ·  {machine}"
        + (f" · seed {seed}" if seed is not None else "")
        + (f" · {model}" if model else "")
        + "\n"
        f"- submitted: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}\n"
        f"- question: {question or '<fill in>'}\n"
        f"- params: `{pj}`\n"
        f"- dir: `results/…_{run_id}/`  · status: submitted  · result: <fill at completion>\n"
    )
    with jp.open("a") as f:
        f.write(stub)


def _emit_exports(run_id: str, slug: str, params: dict, seed: int | None,
                  model: str | None, model_rev: str | None, question: str | None) -> None:
    """Print shell `export` lines for the run script to eval."""
    def sh(v: str) -> str:
        return "'" + v.replace("'", "'\\''") + "'"

    lines = [f"export RUN_ID={sh(run_id)}", f"export JM_SLUG={sh(slug)}"]
    if params:
        lines.append(f"export JM_PARAMS={sh(json.dumps(params, ensure_ascii=False))}")
    if seed is not None:
        lines.append(f"export JM_SEED={sh(str(seed))}")
    if model:
        lines.append(f"export JM_MODEL={sh(model)}")
    if model_rev:
        lines.append(f"export JM_MODEL_REVISION={sh(model_rev)}")
    if question:
        lines.append(f"export JM_NOTES={sh(question)}")
    print("\n".join(lines))


def main() -> int:
    ap = argparse.ArgumentParser(description="Mint run_id + open journal stub + emit exports.")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--machine", default="pace", choices=["pace", "lab", "lenovo-lab"])
    ap.add_argument("--question", default=None)
    ap.add_argument("--params", default=None, help="JSON object of the experiment's independent vars")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--model-revision", default=None)
    ap.add_argument("--repo-root", default=None)
    args = ap.parse_args()

    repo = _repo_root(args.repo_root)
    params: dict = {}
    if args.params:
        try:
            params = json.loads(args.params)
            assert isinstance(params, dict)
        except Exception as e:
            print(f"# --params not a JSON object, ignored: {e}", file=sys.stderr)
            params = {}

    date = time.strftime("%Y-%m-%d")
    run_id = f"r{date}.{args.machine}.{_next_seq(repo, date, args.machine):02d}"

    jp = _journal_path(repo, args.slug)
    _ensure_journal(repo, jp, args.slug, args.question)
    _append_stub(jp, run_id, args.machine, args.question, params, args.seed, args.model)

    # Tell the caller where things landed (stderr, so stdout stays clean for eval)
    print(f"# run_id={run_id}  journal={jp.relative_to(repo)}", file=sys.stderr)
    _emit_exports(run_id, args.slug, params, args.seed, args.model,
                  args.model_revision, args.question)
    return 0


if __name__ == "__main__":
    sys.exit(main())
