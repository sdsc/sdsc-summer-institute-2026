#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive session on the GPU partition
# Usage: bash srun-gpu.sh
#
# Requests an interactive srun on the Expanse GPU shared partition with:
#   1 node, 1 GPU, 10 CPUs, 92 GB memory, 4 hour time limit
#   Account: sdp173

srun \
  --account=sdp173 \
  --partition=gpu-shared \
  --nodes=1 \
  --ntasks-per-node=1 \
  --cpus-per-task=10 \
  --mem=92G \
  --gpus=1 \
  --time=04:00:00 \
  --pty \
  --wait=0 \
  /bin/bash