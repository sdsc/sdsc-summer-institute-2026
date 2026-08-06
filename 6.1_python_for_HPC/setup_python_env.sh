#!/bin/bash
# Install Miniforge to shared project storage and create the pythonhpc env.
# Run once from an Expanse login node (or compute node):
#   bash setup_python_env.sh

set -euo pipefail

INSTALL_DIR="/expanse/lustre/projects/sdp173/zonca"
MINIFORGE_DIR="${INSTALL_DIR}/miniforge3"
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "Downloading Miniforge installer..."
wget -q https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh

echo "Installing Miniforge to ${MINIFORGE_DIR}..."
bash Miniforge3-Linux-x86_64.sh -p "$MINIFORGE_DIR" -b -c
rm Miniforge3-Linux-x86_64.sh

echo "Creating pythonhpc env from environment.yaml..."
source "${MINIFORGE_DIR}/etc/profile.d/conda.sh"
conda env update -n pythonhpc -f "${SCRIPT_DIR}/environment.yaml"

echo "Done. pythonhpc env at ${MINIFORGE_DIR}/envs/pythonhpc"
