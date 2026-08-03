#!/bin/bash
# 
# SDSC Summer Institute 2026
# Deep Learning - Interactive JupyterLab on gpu-shared partition
# Usage: bash launch_galyleo_gpu.sh
#
# Launches a JupyterLab session on the Expanse gpu-shared partition with the following parameters:
#   1 node, 1 GPU, 4 CPUs, 92 GB memory, 4 hour time limit
#   Account: sdp173
#   Singularity container: ptl-cuda-12-1.sif
#
# The reservation and QOS are required for SI26 production sessions.
#
set -euo pipefail

export SI26_DATA_DIR="/cm/shared/examples/sdsc/si/2026"

/cm/shared/apps/sdsc/galyleo/galyleo launch \
  --account sdp173 \
  --partition gpu-shared \
  --gpus 1 \
  --cpus 4 \
  --memory 92 \
  --time-limit 04:00:00 \
  --sif /cm/shared/examples/sdsc/si/2026/ptl-cuda-12-1.sif \
  --reservation si26gpu \
  --qos gpu-shared-eot \
  --cache \
  --bind /expanse,/scratch,/cm \
  --nv \
  --quiet
