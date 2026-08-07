#!/bin/bash
#SBATCH --job-name=create-pythonhpc
#SBATCH --account=sdp173
#SBATCH --partition=compute
#SBATCH --reservation=si26cpu
#SBATCH --qos=normal-eot
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=128
#SBATCH --mem=242G
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%j.out

# Create and cache the pythonhpc conda env once. Sources stage_condaenv.sh,
# which builds the env from environment.yaml, conda-packs it, and caches it in
# ~/.galyleo/pythonhpc/ for Galyleo and the Dask workers to reuse.
#
# The job requests the full node (128 cores) so conda and conda-pack can use
# all available cores during the solve, extraction, and packing.
#
# Run once per institute:
#   sbatch python_expanse.slurm

set -euo pipefail

# Locate stage_condaenv.sh. sbatch copies this script to the spool dir, so
# resolve from the submission directory instead of BASH_SOURCE[0].
SCRIPT_DIR="${SLURM_SUBMIT_DIR:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)}"
if [[ -f "${SCRIPT_DIR}/stage_condaenv.sh" ]]; then
  PYHPC_STAGE_SCRIPT="${SCRIPT_DIR}/stage_condaenv.sh"
else
  PYHPC_STAGE_SCRIPT="${SCRIPT_DIR}/0_python_condaenv_scratch/stage_condaenv.sh"
fi

source "$PYHPC_STAGE_SCRIPT" pythonhpc

echo "pythonhpc env created and cached:"
ls -la "$HOME/.galyleo/pythonhpc/"
