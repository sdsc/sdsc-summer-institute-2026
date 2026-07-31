#!/bin/bash
# Validate local lesson material inside an existing one-node debug allocation.

set -euo pipefail

if [[ "${SLURM_JOB_PARTITION:-}" != "debug" ]]; then
  echo "ERROR: run this script only inside an Expanse debug allocation."
  exit 1
fi

SESSION_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
RESULTS_DIR="${SESSION_ROOT}/test-results"
SIF_PATH="${PYHPC_SIF_PATH:-/expanse/lustre/projects/sds166/zonca/dask-numba-si26.sif}"

cd "$SESSION_ROOT"
mkdir -p "$RESULTS_DIR"

source support/condaenv_scratch/stage_condaenv.sh pythonhpc

python tests/validate_material.py
python support/condaenv_scratch/node_info.py
python tests/execute_local_notebooks.py
mv \
  "$RESULTS_DIR/local-notebooks.json" \
  "$RESULTS_DIR/local-notebooks-conda.json"

if [[ ! -f "$SIF_PATH" ]]; then
  echo "ERROR: Singularity image not found: $SIF_PATH"
  echo "Set PYHPC_SIF_PATH to the image you want to test."
  exit 1
fi

module load singularitypro

singularity exec \
  --bind /expanse \
  --pwd "$SESSION_ROOT" \
  "$SIF_PATH" \
  bash -lc '
    export PYHPC_TEST_MODE=1
    export NUMBA_NUM_THREADS=4
    export OMP_NUM_THREADS=1
    export OPENBLAS_NUM_THREADS=1
    export MKL_NUM_THREADS=1
    python -c "import numpy, numba, dask, distributed, pandas, psutil, graphviz"
    python tests/execute_local_notebooks.py
  '

mv \
  "$RESULTS_DIR/local-notebooks.json" \
  "$RESULTS_DIR/local-notebooks-container.json"

echo "One-node Conda and Singularity validation passed."
echo "Results: $RESULTS_DIR"
