#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive session on the GPU shared partition
# Usage: bash srun-gpu.sh
#
# Requests an interactive srun on the Expanse GPU shared partition with:
#   1 node, 1 GPU, 10 CPUs, 92 GB memory, 4 hour time limit
#   Account: sdp173
#   Reservation: si26gpu (Summer Institute only, remove after institute)
#   QoS: gpu-shared-eot (education, outreach, and training -- Summer Institute only, remove after institute)

exec srun \
  --account=sdp173 \
  --reservation=si26gpu \
  --partition=gpu-shared \
  --qos=gpu-shared-eot \
  --nodes=1 \
  --ntasks-per-node=1 \
  --cpus-per-task=10 \
  --mem=92G \
  --gpus=1 \
  --time=04:00:00 \
  --pty \
  --wait=0 \
  /bin/bash
