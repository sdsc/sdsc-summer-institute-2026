#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive session on the shared partition
# Usage: bash srun-shared.sh
#
# Requests an interactive srun on the Expanse shared partition with:
#   1 node, 4 CPUs, 16 GB memory, 4 hour time limit
#   Account: sdp173

srun \
  --account=sdp173 \
  --partition=shared \
  --nodes=1 \
  --ntasks-per-node=1 \
  --cpus-per-task=4 \
  --mem=16G \
  --time=04:00:00 \
  --pty \
  --wait=0 \
  /bin/bash