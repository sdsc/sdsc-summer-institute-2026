#!/bin/bash
# Launch a Dask worker that connects to the scheduler whose address is stored
# in ~/.dask_scheduler.json. Run this on a compute node, typically via
# dask_workers.slrm from the login node.

set -euo pipefail

SCHEDULER_FILE="${DASK_SCHEDULER_FILE:-$HOME/.dask_scheduler.json}"
WORKER_THREADS="${DASK_WORKER_THREADS:-${SLURM_CPUS_PER_TASK:-1}}"
WORKER_MEMORY="${DASK_WORKER_MEMORY:-auto}"

if [[ ! -f "$SCHEDULER_FILE" ]]; then
    echo "ERROR: scheduler file not found at $SCHEDULER_FILE"
    echo "       Start the scheduler first with launch_scheduler.sh"
    exit 1
fi

echo "Launching dask worker, connecting to scheduler in $SCHEDULER_FILE"
dask worker \
    --scheduler-file "$SCHEDULER_FILE" \
    --nworkers 1 \
    --nthreads "$WORKER_THREADS" \
    --memory-limit "$WORKER_MEMORY" \
    --name "worker-$(hostname)"
