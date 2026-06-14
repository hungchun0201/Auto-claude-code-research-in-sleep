# Run journals

Narrative experiment log (the "why / what-broke" layer). One file per campaign:
`<YYYY-MM>-<slug>.md`, opened automatically by `/gpu-exp-submission` (`pace/log_run.py`).
Each `### <run_id>` anchor maps 1:1 to a machine record — query it with
`pixi run python pace/query.py "run_id='<id>'"`. (The narrative lives here; the
queryable machine layer is `pace/{job_meta.py,query.py}` + `results/*/job_*.json`.)

| campaign | started | question |
|---|---|---|
