#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive debug session for testing
# Usage: bash srun-debug.sh
#
# Requests an interactive srun on the Expanse debug partition with:
#   1 node, 4 CPUs, 16 GB memory, 30 minute time limit
#   Account: sdp173
#   No reservation or QoS -- use this for testing outside institute hours

srun \
  --account=sdp173 \        # Slurm account for the Summer Institute allocation
  --partition=debug \       # Expanse debug partition
  --nodes=1 \               # Request 1 debug node
  --ntasks-per-node=1 \     # 1 task per node
  --cpus-per-task=4 \       # 4 CPUs for the interactive session
  --mem=16G \               # 16 GB memory
  --time=00:30:00 \         # 30 minute time limit
  --pty \                   # Allocate a pseudo-terminal for interactive use
  /bin/bash