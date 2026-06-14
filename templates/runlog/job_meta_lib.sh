#!/bin/bash
# job_meta_lib.sh — source this in your sbatch.
#
# Usage:
#   source /storage/project/r-rs275-0/hlin464/agent-kvcache/pace/job_meta_lib.sh
#   RESULT_DIR=/path/to/results  # must be set
#   jm_write_meta                # after RESULT_DIR + POLICY/JPS/etc are set
#   trap 'jm_write_result $?' EXIT
#
# Optional hints (helps meta be more informative):
#   export JM_MODEL="/path/to/model"
#   export JM_JOBS="/path/to/jobs.json"
#   export JM_BENCH="/path/to/bench.py"
#   export JM_NOTES="what is this run for"     # = the research question
#
# Run-record bridge (normally set for you by `eval "$(pace/log_run.py ...)"`):
#   export RUN_ID="r2026-06-14.pace.01"        # host-agnostic join key (auto-minted if unset)
#   export JM_SLUG="prefetch-pilot"            # campaign slug (journal file + grouping)
#   export JM_PARAMS='{"M":2048,"jps":10}'     # this experiment's independent vars (queryable)
#   export JM_SEED=42                           # captured into repro{} for reproduction
#   export JM_MODEL_REVISION="0e9e39f"         # pins model@revision in repro{}

_JM_LIB_DIR=$(dirname "${BASH_SOURCE[0]}")
_JM_PY=$_JM_LIB_DIR/job_meta.py

jm_write_meta() {
  : "${RESULT_DIR:?RESULT_DIR must be set before jm_write_meta}"
  local sbf="${SLURM_JOB_SCRIPT:-${BASH_SOURCE[1]:-}}"
  python3 "$_JM_PY" meta "$RESULT_DIR" "$sbf" 2>&1 | sed 's/^/[jm] /'
}

jm_write_result() {
  local rc=${1:-$?}
  : "${RESULT_DIR:?RESULT_DIR must be set before jm_write_result}"
  python3 "$_JM_PY" result "$RESULT_DIR" "$rc" 2>&1 | sed 's/^/[jm] /'
}
