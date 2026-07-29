#!/bin/bash
# Launch a Dask distributed scheduler on this node.
#
# Run this inside a JupyterLab terminal so the scheduler is on the same node
# as the notebook that will connect to it.
#
# The scheduler writes its address to ~/.dask_scheduler.json, which the worker
# job reads to find the scheduler.

set -euo pipefail

SCHEDULER_FILE="${DASK_SCHEDULER_FILE:-$HOME/.dask_scheduler.json}"

# Bind the scheduler to the node's public IP so worker nodes on other hosts
# can reach it. The dashboard runs on :8787 for the Dask Lab Extension.
PUBLIC_IP="${DASK_SCHEDULER_HOST:-$(hostname -I | awk '{print $1}')}"

echo "Launching dask scheduler on $PUBLIC_IP:8786"
echo "Dashboard: http://$PUBLIC_IP:8787/status"
echo "Scheduler file: $SCHEDULER_FILE"
echo "Waiting for workers. You will see a line each time one connects."
echo

dask scheduler \
    --scheduler-file "$SCHEDULER_FILE" \
    --host "$PUBLIC_IP" \
    --port 8786 \
    --dashboard-address ":8787"
