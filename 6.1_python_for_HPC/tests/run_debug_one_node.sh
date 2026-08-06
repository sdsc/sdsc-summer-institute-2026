#!/bin/bash
# Validate local lesson material inside an existing one-node debug allocation.

set -euo pipefail

if [[ "${SLURM_JOB_PARTITION:-}" != "debug" ]]; then
  echo "ERROR: run this script only inside an Expanse debug allocation."
  exit 1
fi

SESSION_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
RESULTS_DIR="${SESSION_ROOT}/test-results"
export PYHPC_CONDA_ACTIVATE="/expanse/lustre/projects/sdp173/zonca/miniforge3/envs/pythonhpc/bin/activate"

cd "$SESSION_ROOT"
mkdir -p "$RESULTS_DIR"

source "$PYHPC_CONDA_ACTIVATE"

python tests/validate_material.py
python support/condaenv_scratch/node_info.py
python tests/execute_local_notebooks.py

echo "One-node validation passed."
echo "Results: $RESULTS_DIR"
