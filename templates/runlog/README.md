# templates/runlog — canonical experiment-record machinery

Copied into every new ARIS project by `aris-init` (Phase 1). The host-agnostic
experiment-record system: machine layer (`job_meta.py` + `query.py` + sidecars +
`submissions/results.jsonl`) joined to the narrative layer (`runlog/<YYYY-MM>-<slug>.md`)
by a `run_id`, dispatched via the `/gpu-exp-submission` skill. Spec:
`../../skills/shared-references/experiment-record.md`.

On copy, `job_meta.py`'s `__PROJECT_REPO__` / `__ENGINE_ROOM__` are sed-patched to the
project's paths. `job_meta_lib.sh`, `log_run.py`, `query.py` are path-agnostic (git rev-parse).
Files land in the project as: `pace/{job_meta.py,job_meta_lib.sh,log_run.py,query.py}` +
`runlog/{_TEMPLATE.md,INDEX.md}`.
