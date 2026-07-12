#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive session on the compute partition
# Usage: bash srun-compute.sh
#
# Requests an interactive srun on the Expanse compute partition with:
#   1 node, 128 CPUs, 242 GB memory, 4 hour time limit
#   Account: sdp173

srun \
  --account=sdp173 \
  --partition=compute \
  --nodes=1 \
  --ntasks-per-node=1 \
  --cpus-per-task=128 \
  --mem=242G \
  --time=04:00:00 \
  --pty \
  --wait=0 \
  /bin/bash