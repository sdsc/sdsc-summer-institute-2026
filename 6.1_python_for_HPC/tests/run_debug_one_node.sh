#!/bin/bash
# Validate local lesson material inside an existing one-node debug allocation.

set -euo pipefail

if [[ "${SLURM_JOB_PARTITION:-}" != "debug" ]]; then
  echo "ERROR: run this script only inside an Expanse debug allocation."
  exit 1
fi

SESSION_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
RESULTS_DIR="${SESSION_ROOT}/test-results"

cd "$SESSION_ROOT"
mkdir -p "$RESULTS_DIR"

# Stage the shared pythonhpc conda env onto node-local scratch, then run the
# validation steps from it. First run builds and caches the env.
source 0_python_condaenv_scratch/stage_condaenv.sh pythonhpc

python tests/validate_material.py
python 0_python_condaenv_scratch/node_info.py
python tests/execute_local_notebooks.py

echo "One-node validation passed."
echo "Results: $RESULTS_DIR"
