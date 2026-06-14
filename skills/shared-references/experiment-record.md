# Experiment-record system — spec

The host-agnostic, reproducible experiment record shared by `gpu-exp-submission`,
`pace-slurm-submit`, `monitor-experiment`, and `experiment-audit`. Machinery template:
`templates/runlog/`. Goal: from any record, fully reproduce the run weeks later — on PACE,
lab, or lenovo-lab.

## Three layers, joined by `run_id`

1. **Machine layer** — `pace/job_meta.py` writes `job_meta.json` (submit) + `job_result.json`
   (exit) sidecars into `results/<exp>_<gpu>_<run_id>/`, and appends `pace/submissions.jsonl`
   / `pace/results.jsonl`. `pace/query.py` materialises an in-memory DuckDB `runs` view over
   them (always fresh; `runs.duckdb` is a gitignored cache). **JSONL is canonical, DuckDB is the lens.**
2. **Narrative layer** — `runlog/<YYYY-MM>-<slug>.md` (one file per campaign) + `runlog/INDEX.md`
   from `runlog/_TEMPLATE.md`. Each `### <run_id>` anchor == one machine record. Keeps the
   gold: research question, **issue→fix table**, results matrix with seeds + job-counts.
3. **Bridge** — `pace/log_run.py` (the dispatcher half) mints the `run_id`, opens the journal
   stub, and emits `export RUN_ID/JM_*` lines the run script `eval`s, so `job_meta.py` stamps
   the same id. One key, written on both sides at submit time.

## `run_id`
`r<YYYY-MM-DD>.<machine>.<NN>` — sortable, human-typeable, machine-scoped (collision-safe across
hosts). Minted single-process by `log_run.py` (pretty sequential) → fan-out peers never race.
Bare-job fallback in `job_meta.py`: `r<date>.pace.<slurm_job_id>` (SLURM) or `r<date>.<host>.<pid>`
(local) — unique without a shared counter. `slurm_job_id` is an optional field, never the key.

## Schema (job_meta.json, schema_version 2)
Adds to the existing capture: `run_id`, `slug`, `host_kind` (`slurm|local`), `params{}`,
`repro{}`. `host_kind=slurm` → SLURM branch (+ sacct); else local (host + PID + nvidia-smi).

- **`params{}`** — the experiment's *independent variables* (free-form JSON from `JM_PARAMS`).
  Queryable via `params->>'<knob>'`, NULL where a knob doesn't apply. Lets heterogeneous
  experiments A and B coexist in one DuckDB **without editing query.py**. Curated headline metrics
  still use the `bench_kind` discriminator + per-kind extraction (unified columns).
- **`repro{}`** — `env_lock` (`pixi.lock@<sha>` / `conda-lock@<sha>` / `conda-export(loose)`),
  `seed`, `model` (id@revision), `code_sha`, `code_dirty`, `engine_sha`, `engine_dirty`.

## Reproducibility contract (R1)
A keeper run requires `code_dirty=false` (commit first) and a frozen `env_lock`
(`pixi.lock` is bit-exact by default; conda needs `conda-lock --kind explicit`). With those plus
the captured sbatch + `gpu.uuid/driver` + `seed` + `model@rev` + `params`, the run rebuilds
identically up to documented nondeterminism (changed GPU/driver, nondeterministic kernels —
captured, not hidden).

## Env vars the dispatcher exports (read by job_meta.py)
`RUN_ID, JM_SLUG, JM_PARAMS (JSON), JM_SEED, JM_MODEL, JM_MODEL_REVISION, JM_NOTES (=question)`.
Normally set by `eval "$(pace/log_run.py --slug … --machine … --question … --params … --seed … --model …)"`.

## Trigger & enforcement
Recording fires at the **run-script level** (`jm_write_meta` start + `trap jm_write_result $? EXIT`),
host-agnostic. `gpu-exp-submission` is the front door that always injects these + opens the journal.
PACE watch-or-die is Stop-hook-enforced (`pace-watch-guard.py`); lab/lenovo-lab watch is
skill-enforced (hook generalization is a follow-up).

## Skill integration
- `experiment-audit` SHOULD fail if a cited result's `run_id` has no `runlog/` journal anchor
  (machine/narrative drift = integrity flag).
- `monitor-experiment` MAY update the ledger (`write_result`) on completion for near-automatic status.
