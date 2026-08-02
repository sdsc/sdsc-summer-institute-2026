#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive session on the compute partition
# Usage: bash srun-compute.sh
#
# Requests an interactive srun on the Expanse compute partition with:
#   1 node, 128 CPUs, 242 GB memory, 4 hour time limit
#   Account: sdp173
#   Reservation: si26cpu (Summer Institute only, remove after institute)
#   QoS: normal-eot (education, outreach, and training -- Summer Institute only, remove after institute)

srun_args=(
  --account=sdp173        # Slurm account for the Summer Institute allocation
  --reservation=si26cpu   # Summer Institute CPU reservation (remove after institute)
  --partition=compute     # Expanse compute partition
  --qos=normal-eot        # Education, outreach, and training QoS (remove after institute)
  --nodes=1               # Request 1 compute node
  --ntasks-per-node=1     # 1 task per node
  --cpus-per-task=128     # 128 CPUs for the interactive session
  --mem=242G              # 242 GB memory
  --time=04:00:00         # 4 hour time limit
  --pty                    # Allocate a pseudo-terminal for interactive use
  --wait=0                 # Do not wait for remaining tasks after the first task exits
)

srun "${srun_args[@]}" /bin/bash
