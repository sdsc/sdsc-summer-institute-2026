#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive session on the GPU shared partition
# Usage: bash srun-gpu.sh
#
# Requests an interactive srun on the Expanse GPU shared partition with:
#   1 node, 1 GPU, 10 CPUs, 92 GB memory, 4 hour time limit
#   Account: sdp173
#   Reservation: si26gpu (Summer Institute only, remove after institute)
#   QoS: gpu-shared-eot (education, outreach, and training -- Summer Institute only, remove after institute)

srun_args=(
  --account=sdp173        # Slurm account for the Summer Institute allocation
  --reservation=si26gpu   # Summer Institute GPU reservation (remove after institute)
  --partition=gpu-shared  # Expanse GPU shared partition
  --qos=gpu-shared-eot    # Education, outreach, and training QoS (remove after institute)
  --nodes=1               # Request 1 GPU node
  --ntasks-per-node=1     # 1 task per node
  --cpus-per-task=10      # 10 CPUs for the interactive session
  --mem=92G               # 92 GB memory
  --gpus=1                # 1 GPU
  --time=04:00:00         # 4 hour time limit
  --pty                    # Allocate a pseudo-terminal for interactive use
  --wait=0                 # Do not wait for remaining tasks after the first task exits
)

srun "${srun_args[@]}" /bin/bash
