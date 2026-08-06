#!/bin/bash
# SDSC Summer Institute 2026 -- Python for HPC: Interactive JupyterLab on compute partition
# Usage: bash launch_galyleo_compute.sh
#
# Launches a JupyterLab session on the Expanse compute partition with:
#   1 node, 128 CPUs, 242 GB memory, 4 hour time limit
#   Account: sdp173
#   Conda env: pythonhpc (installed on shared project storage by setup_python_env.sh)
#
# The reservation and QOS are required for SI26 production sessions.
# Instructors should use TESTING.md and the debug queue before the institute.

set -euo pipefail

NOTEBOOK_FOLDER=$(pwd -P)
export PYHPC_MINIFORGE_DIR="/expanse/lustre/projects/sdp173/zonca/miniforge3"

/cm/shared/apps/sdsc/galyleo/galyleo launch \
  --account sdp173 \
  --partition compute \
  --reservation si26cpu \
  --qos normal-eot \
  --cpus 128 \
  --memory 242 \
  --time-limit 04:00:00 \
  --conda-init "${PYHPC_MINIFORGE_DIR}" \
  --conda-env pythonhpc \
  --notebook-dir "${NOTEBOOK_FOLDER}" \
  --interface lab \
  --quiet
