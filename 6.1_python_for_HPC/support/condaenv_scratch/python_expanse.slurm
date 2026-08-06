#!/bin/bash
#SBATCH --job-name=node-info
#SBATCH --account=sdp173
#SBATCH --partition=compute
#SBATCH --reservation=si26cpu
#SBATCH --qos=normal-eot
#SBATCH --nodes=2
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=128
#SBATCH --mem=242G
#SBATCH --time=00:05:00
#SBATCH --output=slurm-%j.out

set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export PYHPC_NODE_INFO="${SCRIPT_DIR}/node_info.py"
export PYHPC_CONDA_ACTIVATE="/expanse/lustre/projects/sdp173/zonca/miniforge3/envs/pythonhpc/bin/activate"

echo "Running on nodes:"
scontrol show hostname "$SLURM_NODELIST"

srun --exact --ntasks=2 --ntasks-per-node=1 --unbuffered \
    bash -c 'source "$PYHPC_CONDA_ACTIVATE" && exec python "$PYHPC_NODE_INFO"'
