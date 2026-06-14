#!/usr/bin/env python3
"""job_meta — capture job settings + results as sidecar JSON.

Import-time free of vllm; safe to call at sbatch start and from login node."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

_PROJECT_REPO_DEFAULT = "__PROJECT_REPO__"  # patched by aris-init (sed)
ENGINE_ROOM = "__ENGINE_ROOM__"  # patched by aris-init (sed)


def _resolve_repo(default: str) -> str:
    """Host-agnostic repo root: the configured PACE path if it exists, else the
    git repo containing cwd (lab / lenovo-lab / local), else the default."""
    if Path(default).exists():
        return default
    try:
        top = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL, text=True,
        ).strip()
        return top or default
    except Exception:
        return default


PROJECT_REPO = _resolve_repo(_PROJECT_REPO_DEFAULT)
INDEX_SUBMIT = Path(PROJECT_REPO) / "pace/submissions.jsonl"
INDEX_RESULT = Path(PROJECT_REPO) / "pace/results.jsonl"
MAX_DIFF_BYTES = 1_000_000  # cap git diff capture to 1 MB


def _sh(cmd: list[str], timeout: int = 30) -> str | None:
    try:
        return subprocess.check_output(
            cmd, stderr=subprocess.DEVNULL, text=True, timeout=timeout
        ).strip()
    except Exception:
        return None


def _sha256_file(p: Path) -> str | None:
    h = hashlib.sha256()
    try:
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def _git_info(repo: str) -> dict:
    if not Path(repo).exists():
        return {"path": repo, "present": False}
    d = {"path": repo, "present": True}
    d["sha"] = _sh(["git", "-C", repo, "rev-parse", "HEAD"])
    d["branch"] = _sh(["git", "-C", repo, "rev-parse", "--abbrev-ref", "HEAD"])
    rc = subprocess.call(
        ["git", "-C", repo, "diff", "--quiet"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    d["dirty"] = rc != 0
    if d["dirty"]:
        diff = _sh(["git", "-C", repo, "diff", "HEAD"], timeout=60) or ""
        d["diff_bytes"] = len(diff.encode())
        d["diff_truncated"] = len(diff.encode()) > MAX_DIFF_BYTES
        d["diff"] = diff[:MAX_DIFF_BYTES]
    return d


def _relevant_env() -> dict:
    prefixes = ("SCHED_TRACE_", "LMCACHE_", "VLLM_", "CUDA_", "TORCH_", "TRITON_", "HF_", "SLURM_")
    singles = (
        "CPU_BYTES", "CPU_LARGE_BYTES", "CPU_SMALL_BYTES",
        "POLICY", "JPS", "DRAM_GB", "GPU_TAG", "NUM_JOBS", "LIMIT",
        "TRACE_MAX_STEPS", "DURATION", "CONDA_PREFIX",
        "JM_MODEL", "JM_JOBS", "JM_BENCH", "JM_NOTES",
        # run-record bridge (host-agnostic id, experiment vars, reproducibility)
        "RUN_ID", "JM_SLUG", "JM_PARAMS", "JM_SEED", "SEED", "JM_MODEL_REVISION",
        "PIXI_ENVIRONMENT_NAME",
    )
    out = {}
    for k, v in os.environ.items():
        if k.startswith(prefixes) or k in singles:
            out[k] = v
    return out


def _gpu_info() -> dict:
    name = _sh(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"])
    if not name:
        return {"present": False}
    return {
        "present": True,
        "name": name,
        "memory_total": _sh(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader"]),
        "driver": _sh(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"]),
        "uuid": _sh(["nvidia-smi", "--query-gpu=uuid", "--format=csv,noheader"]),
    }


def _env_versions() -> dict:
    py_bin = os.environ.get("CONDA_PREFIX", "")
    if py_bin:
        py_bin = f"{py_bin}/bin/python3"
    if not py_bin or not Path(py_bin).exists():
        py_bin = "python3"
    return {
        "python_bin": py_bin,
        "python_version": _sh([py_bin, "--version"]),
        "vllm_version": _sh([py_bin, "-c", "import vllm; print(vllm.__version__)"]),
        "vllm_file": _sh([py_bin, "-c", "import vllm; print(vllm.__file__)"]),
        "torch_version": _sh([py_bin, "-c", "import torch; print(torch.__version__)"]),
        "torch_cuda": _sh([py_bin, "-c", "import torch; print(torch.version.cuda)"]),
    }


def _conda_env_export() -> str | None:
    env_path = os.environ.get("CONDA_PREFIX")
    if not env_path:
        return None
    # --no-builds strips build hashes for portability; --prefix uses env dir
    return _sh(["conda", "env", "export", "--no-builds", "--prefix", env_path], timeout=120)


def _host_kind() -> str:
    """'slurm' on PACE (SLURM_JOB_ID present), else 'local' (lab / lenovo-lab)."""
    return "slurm" if os.environ.get("SLURM_JOB_ID") else "local"


def _short_host() -> str:
    """Short, filesystem-safe host token for the run_id (e.g. 'lab', 'px2')."""
    node = os.uname().nodename.split(".")[0].lower()
    return "".join(c if c.isalnum() else "-" for c in node)[:12] or "host"


def _mint_run_id() -> str:
    """Host-agnostic run identity, the join key across machines.

    Preference order, so fan-out jobs never collide:
    1. RUN_ID exported by the dispatcher (`/gpu-exp-submission` mints the pretty
       sequential `r<date>.pace.NN` once per submit, before fan-out).
    2. Fallback for a bare job: a race-free id keyed on the unique SLURM job id
       (PACE) or the PID (lab/lenovo-lab) — no shared counter, no collision.
    """
    rid = os.environ.get("RUN_ID")
    if rid:
        return rid
    date = time.strftime("%Y-%m-%d")
    sjid = os.environ.get("SLURM_JOB_ID")
    if sjid:
        return f"r{date}.pace.{sjid}"
    return f"r{date}.{_short_host()}.{os.getpid()}"


def _params(extra: dict | None) -> dict:
    """The experiment's independent variables (free-form; complements env_vars).

    Sourced from JM_PARAMS (a JSON object string the dispatcher exports) merged
    with any `extra` passed in code. Lets a NEW knob be queried via
    `params->>'<knob>'` without editing query.py.
    """
    out: dict = {}
    raw = os.environ.get("JM_PARAMS")
    if raw:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                out.update(parsed)
        except Exception as e:
            print(f"[jm] JM_PARAMS not valid JSON, ignored: {e}", file=sys.stderr)
    if extra:
        out.update(extra)
    return out


def _env_lock() -> str | None:
    """Pointer to a FROZEN environment lock (bit-exact repro), if one exists.

    pixi.lock is bit-exact by default; conda needs a conda-lock explicit file.
    Falls back to a 'conda-export(loose)' marker (the full export still lives in
    `conda_env_export`, but a loose export can re-resolve — not bit-exact)."""
    pixi_lock = Path(PROJECT_REPO) / "pixi.lock"
    if pixi_lock.is_file():
        return f"pixi.lock@{_sha256_file(pixi_lock)}"
    conda_lock = Path(PROJECT_REPO) / "repro" / "env.lock"
    if conda_lock.is_file():
        return f"conda-lock@{_sha256_file(conda_lock)}"
    if os.environ.get("CONDA_PREFIX"):
        return "conda-export(loose)"
    return None


def _seed() -> int | None:
    raw = os.environ.get("JM_SEED") or os.environ.get("SEED")
    try:
        return int(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None


def _repro_block(git: dict) -> dict:
    """Everything needed to rebuild this run weeks later (R1)."""
    proj = git.get("project", {})
    eng = git.get("engine_room", {})
    model = os.environ.get("JM_MODEL")
    rev = os.environ.get("JM_MODEL_REVISION")
    return {
        "env_lock": _env_lock(),
        "seed": _seed(),
        "model": f"{model}@{rev}" if (model and rev) else model,
        "code_sha": proj.get("sha"),
        "code_dirty": proj.get("dirty"),
        "engine_sha": eng.get("sha") if eng.get("present") else None,
        "engine_dirty": eng.get("dirty") if eng.get("present") else None,
    }


def write_meta(result_dir: str, sbatch_file: str | None = None,
               extra: dict | None = None) -> Path:
    """Write job_meta.json into result_dir. Returns the path."""
    rd = Path(result_dir)
    rd.mkdir(parents=True, exist_ok=True)
    meta_path = rd / "job_meta.json"

    run_id = _mint_run_id()
    slug = os.environ.get("JM_SLUG") or os.environ.get("SLURM_JOB_NAME") or rd.name
    git = {
        "project": _git_info(PROJECT_REPO),
        "engine_room": _git_info(ENGINE_ROOM),
    }
    params = _params(extra)

    meta = {
        "schema_version": 2,
        "run_id": run_id,
        "slug": slug,
        "host_kind": _host_kind(),
        "submit_ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "host": os.uname().nodename,
        "cwd": os.getcwd(),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "slurm_job_name": os.environ.get("SLURM_JOB_NAME"),
        "gpu": _gpu_info(),
        "params": params,
        "repro": _repro_block(git),
        "env_versions": _env_versions(),
        "conda_env_export": _conda_env_export(),
        "env_vars": _relevant_env(),
        "git": git,
    }

    if sbatch_file and Path(sbatch_file).is_file():
        p = Path(sbatch_file)
        meta["sbatch"] = {
            "path": str(p),
            "sha256": _sha256_file(p),
            "size": p.stat().st_size,
            "mtime": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(p.stat().st_mtime)),
            "content": p.read_text(errors="replace"),
        }

    if extra:
        meta["extra"] = extra

    meta_path.write_text(json.dumps(meta, indent=2, default=str))

    # Append submissions index
    _append_index(INDEX_SUBMIT, {
        "ts": meta["submit_ts"],
        "run_id": run_id,
        "slug": slug,
        "host_kind": meta["host_kind"],
        "job_id": meta["slurm_job_id"],
        "job_name": meta["slurm_job_name"],
        "gpu_tag": os.environ.get("GPU_TAG"),
        "policy": os.environ.get("POLICY"),
        "jps": os.environ.get("JPS"),
        "params": params,
        "question": os.environ.get("JM_NOTES"),
        "result_dir": str(rd),
        "meta_path": str(meta_path),
    })
    return meta_path


def _append_index(path: Path, row: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as f:
            f.write(json.dumps(row, default=str) + "\n")
    except Exception as e:
        print(f"[jm] index append failed: {e}", file=sys.stderr)


def _run_id_from_sidecar(rd: Path) -> str | None:
    """Recover the run_id minted at write_meta time (host-agnostic join key)."""
    try:
        meta = json.loads((rd / "job_meta.json").read_text())
        return meta.get("run_id")
    except Exception:
        return None


def write_result(result_dir: str, shell_rc: int = 0) -> Path:
    rd = Path(result_dir)
    job_id = os.environ.get("SLURM_JOB_ID", "")
    run_id = os.environ.get("RUN_ID") or _run_id_from_sidecar(rd) or _mint_run_id()
    result: dict = {
        "schema_version": 2,
        "run_id": run_id,
        "end_ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "job_id": job_id or None,
        "shell_rc": shell_rc,
    }

    # sacct
    if job_id:
        sa = _sh([
            "sacct", "-j", job_id, "--noheader", "--parsable2",
            "--format=JobID,State,ExitCode,Elapsed,CPUTime,MaxRSS,NodeList,ReqTRES",
        ])
        if sa:
            rows = []
            for line in sa.splitlines():
                parts = line.split("|")
                if "." in parts[0]:
                    continue  # skip .batch/.extern substeps
                keys = ["job_id", "state", "exit_code", "elapsed",
                        "cpu_time", "max_rss", "nodelist", "req_tres"]
                rows.append(dict(zip(keys, parts)))
            if rows:
                result["sacct"] = rows[0]

    # Artefacts
    artefacts = []
    for p in sorted(rd.glob("*")):
        if p.is_file() and p.name not in ("job_meta.json", "job_result.json"):
            artefacts.append({
                "name": p.name,
                "size": p.stat().st_size,
                "sha256": _sha256_file(p) if p.stat().st_size < 500_000_000 else None,
            })
    result["artefacts"] = artefacts

    # Bench summary — supports both ab_benchmark.py and swe_replay_benchmark.py output schemas
    # ab:  avg_duration_s / p90_duration_s / completed_jobs / total_jobs / errors / median_duration_s
    # swe: avg_job_duration_s / median_job_duration_s / total_wall_s / n_jobs (no p90/p95/errors)
    for bj in sorted(rd.glob("*_jps*.json")):
        try:
            d = json.loads(bj.read_text())
            result["bench_summary"] = {
                "file": bj.name,
                "policy": d.get("policy"),
                "jps": d.get("jps"),
                # Total job count (try both schemas)
                "total_jobs": d.get("total_jobs") or d.get("n_jobs"),
                "completed_jobs": d.get("completed_jobs") or d.get("n_jobs"),
                "errors": d.get("errors"),
                # Wall clock for whole bench
                "duration_s": d.get("duration_s") or d.get("total_wall_s"),
                # Per-job duration distribution (unified key: avg_duration_s)
                "avg_duration_s": d.get("avg_duration_s") or d.get("avg_job_duration_s"),
                "median_duration_s": d.get("median_duration_s") or d.get("median_job_duration_s"),
                "p90_duration_s": d.get("p90_duration_s"),
                "p95_duration_s": d.get("p95_duration_s"),
                # Discriminator: which bench script
                "bench_kind": ("swe_replay" if "avg_job_duration_s" in d
                                else "ab_benchmark" if "avg_duration_s" in d
                                else "unknown"),
            }
            break
        except Exception:
            pass

    # Error signatures (grep logs)
    sigs = []
    for log in list(rd.glob("*server.log")) + list(rd.glob("*.err")):
        try:
            txt = log.read_text(errors="ignore")[-200_000:]  # last 200KB
            for pat in ("Traceback", "CUDA error", "out of memory",
                        "CUDA out of memory", "SIGKILL", "SIGSEGV",
                        "NCCL", "RuntimeError:"):
                if pat in txt:
                    sigs.append({"log": log.name, "pattern": pat})
        except Exception:
            pass
    result["error_signatures"] = sigs

    result_path = rd / "job_result.json"
    result_path.write_text(json.dumps(result, indent=2, default=str))

    _append_index(INDEX_RESULT, {
        "ts": result["end_ts"],
        "run_id": run_id,
        "job_id": result["job_id"],
        "shell_rc": shell_rc,
        "state": result.get("sacct", {}).get("state"),
        "elapsed": result.get("sacct", {}).get("elapsed"),
        "result_dir": str(rd),
        "result_path": str(result_path),
    })
    return result_path


if __name__ == "__main__":
    # CLI: python job_meta.py {meta|result} <result_dir> [sbatch_file]
    cmd = sys.argv[1]
    rd = sys.argv[2]
    if cmd == "meta":
        sbf = sys.argv[3] if len(sys.argv) > 3 else None
        print(write_meta(rd, sbf))
    elif cmd == "result":
        rc = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        print(write_result(rd, rc))
    else:
        print(f"unknown cmd: {cmd}", file=sys.stderr)
        sys.exit(2)
