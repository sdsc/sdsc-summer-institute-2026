#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive debug session for testing
# Usage: bash srun-debug.sh
#
# Requests an interactive srun on the Expanse debug partition with:
#   1 node, 4 CPUs, 16 GB memory, 30 minute time limit
#   Account: sdp173
#   No reservation or QoS -- use this for testing outside institute hours

exec srun \
  --account=sdp173 \
  --partition=debug \
  --nodes=1 \
  --ntasks-per-node=1 \
  --cpus-per-task=4 \
  --mem=16G \
  --time=00:30:00 \
  --pty \
  /bin/bash
