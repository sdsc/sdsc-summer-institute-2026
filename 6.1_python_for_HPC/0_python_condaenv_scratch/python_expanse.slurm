#!/bin/bash
#SBATCH --job-name=create-pythonhpc
#SBATCH --account=sdp173
#SBATCH --partition=compute
#SBATCH --reservation=si26cpu
#SBATCH --qos=normal-eot
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%j.out

# Create and cache the pythonhpc conda env once. Sources stage_condaenv.sh,
# which builds the env from environment.yaml, conda-packs it, and caches it in
# ~/.galyleo/pythonhpc/ for Galyleo and the Dask workers to reuse.
#
# Run once per institute:
#   sbatch python_expanse.slurm

set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export PYHPC_STAGE_SCRIPT="${SCRIPT_DIR}/stage_condaenv.sh"

source "$PYHPC_STAGE_SCRIPT" pythonhpc

echo "pythonhpc env created and cached:"
ls -la "$HOME/.galyleo/pythonhpc/"
