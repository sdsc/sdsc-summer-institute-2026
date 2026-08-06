#!/bin/bash
# Validate the multi-node capstone inside an existing two-node debug allocation.

set -euo pipefail

if [[ "${SLURM_JOB_PARTITION:-}" != "debug" && "${SLURM_JOB_PARTITION:-}" != "compute" ]]; then
  echo "ERROR: run this script only inside an Expanse debug or compute allocation."
  exit 1
fi

ALLOCATED_NODES="${SLURM_JOB_NUM_NODES:-${SLURM_NNODES:-0}}"

if [[ "$ALLOCATED_NODES" -lt 2 ]]; then
  echo "ERROR: this test requires at least two allocated debug nodes."
  exit 1
fi

SESSION_ROOT="${SLURM_SUBMIT_DIR:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)}"
RESULTS_DIR="${SESSION_ROOT}/test-results"
mkdir -p "$RESULTS_DIR"

RUN_DIR=$(mktemp -d "${RESULTS_DIR}/dask-debug.XXXXXX")
SCHEDULER_FILE="${RUN_DIR}/scheduler.json"
SCHEDULER_LOG="${RUN_DIR}/scheduler.log"
WORKER_LOG="${RUN_DIR}/workers.log"
NOTEBOOK_LOG="${RUN_DIR}/notebook.log"
FIRST_NODE=$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n 1)
SIF_PATH="${PYHPC_SIF_PATH:-/expanse/lustre/projects/sds166/zonca/dask-numba-si26.sif}"
export PYHPC_WORKER_SCRIPT="${SESSION_ROOT}/dask_slurm/launch_worker.sh"

if [[ ! -f "$SIF_PATH" ]]; then
    echo "ERROR: Singularity image not found: $SIF_PATH"
    echo "       Set PYHPC_SIF_PATH to the image you want to use."
    exit 1
fi

cleanup() {
  if [[ -n "${WORKER_STEP_PID:-}" ]]; then
    kill "$WORKER_STEP_PID" 2>/dev/null || true
    wait "$WORKER_STEP_PID" 2>/dev/null || true
  fi
  if [[ -n "${SCHEDULER_STEP_PID:-}" ]]; then
    kill "$SCHEDULER_STEP_PID" 2>/dev/null || true
    wait "$SCHEDULER_STEP_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

module load singularitypro

echo "Starting scheduler on ${FIRST_NODE}"
srun --overlap \
  --cpu-bind=none \
  --nodes=1 \
  --nodelist="$FIRST_NODE" \
  --ntasks=1 \
  --cpus-per-task=1 \
  singularity exec --bind /expanse "$SIF_PATH" \
  dask scheduler --scheduler-file "$SCHEDULER_FILE" --port 0 --dashboard-address :0 \
  >"$SCHEDULER_LOG" 2>&1 &
SCHEDULER_STEP_PID=$!

for _ in $(seq 1 60); do
  [[ -s "$SCHEDULER_FILE" ]] && break
  sleep 1
done
if [[ ! -s "$SCHEDULER_FILE" ]]; then
  echo "ERROR: scheduler did not create $SCHEDULER_FILE"
  sed -n '1,200p' "$SCHEDULER_LOG"
  exit 1
fi

echo "Starting one four-thread worker on each allocated node"
srun --overlap \
   --cpu-bind=none \
   --nodes="$ALLOCATED_NODES" \
   --ntasks="$ALLOCATED_NODES" \
   --ntasks-per-node=1 \
   --cpus-per-task=4 \
   env DASK_SCHEDULER_FILE="$SCHEDULER_FILE" \
       DASK_WORKER_THREADS=4 \
       DASK_WORKER_MEMORY=12GB \
       PYHPC_WORKER_SCRIPT="$PYHPC_WORKER_SCRIPT" \
   singularity exec --bind /expanse "$SIF_PATH" \
   bash -c 'exec "$PYHPC_WORKER_SCRIPT"' \
   >"$WORKER_LOG" 2>&1 &
WORKER_STEP_PID=$!

export DASK_SCHEDULER_FILE="$SCHEDULER_FILE"
export PYHPC_TEST_MODE=1

singularity exec --bind /expanse "$SIF_PATH" python - <<'PY' >"$NOTEBOOK_LOG" 2>&1
import os
from distributed import Client

client = Client(scheduler_file=os.environ["DASK_SCHEDULER_FILE"])
client.wait_for_workers(2, timeout=120)
workers = client.scheduler_info()["workers"]
hosts = {worker["host"] for worker in workers.values()}
assert len(workers) >= 2, workers
assert len(hosts) >= 2, hosts
print(f"Workers: {len(workers)}")
print(f"Hosts: {sorted(hosts)}")
client.close()
PY

singularity exec --bind /expanse "$SIF_PATH" \
python -m jupyter nbconvert \
  --to notebook \
  --execute "$SESSION_ROOT/3_dask/4_multinode_distributed_array.ipynb" \
  --ExecutePreprocessor.timeout=300 \
  --output-dir "$RUN_DIR" \
  --output "capstone.executed.ipynb" \
  >>"$NOTEBOOK_LOG" 2>&1

echo "Multi-node debug validation passed."
echo "Logs: $RUN_DIR"
