#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive session on the shared partition
# Usage: bash srun-shared.sh
#
# Requests an interactive srun on the Expanse shared partition with:
#   1 node, 4 CPUs, 16 GB memory, 4 hour time limit
#   Account: sdp173
#   Reservation: si26cpu (Summer Institute only, remove after institute)
#   Note: No QoS flag needed for shared partition (no shared-eot QoS exists)

srun \
  --account=sdp173 \        # Slurm account for the Summer Institute allocation
  --reservation=si26cpu \   # Summer Institute CPU reservation (remove after institute)
  --partition=shared \      # Expanse shared partition
  --nodes=1 \               # Request 1 shared node
  --ntasks-per-node=1 \     # 1 task per node
  --cpus-per-task=4 \       # 4 CPUs for the interactive session
  --mem=16G \               # 16 GB memory
  --time=04:00:00 \         # 4 hour time limit
  --pty \                   # Allocate a pseudo-terminal for interactive use
  --wait=0 \                # Wait up to 0 seconds (fail immediately if not ready)
  /bin/bash