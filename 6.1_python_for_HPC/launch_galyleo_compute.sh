#!/bin/bash
# SDSC Summer Institute 2026 -- Python for HPC: Interactive JupyterLab on compute partition
# Usage: bash launch_galyleo_compute.sh
#
# Launches a JupyterLab session on the Expanse compute partition with:
#   1 node, 128 CPUs, 242 GB memory, 4 hour time limit
#   Account: sdp173
#   Conda environment from environment.yaml (cached via conda-pack)

NOTEBOOK_FOLDER=$(pwd -P)  # Use current folder as the notebook working directory

/cm/shared/apps/sdsc/galyleo/galyleo launch \
  --account sdp173 \
  --partition compute \
  --cpus 128 \
  --memory 242 \
  --time-limit 04:00:00 \
  --conda-yml environment.yaml \
  --notebook-dir ${NOTEBOOK_FOLDER} \
  --interface lab \
  --cache \
  --quiet
