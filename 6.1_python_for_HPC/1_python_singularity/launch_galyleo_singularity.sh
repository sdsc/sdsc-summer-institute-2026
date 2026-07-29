#!/bin/bash
# SDSC Summer Institute 2026 -- Python for HPC: Singularity container on shared partition
# Usage: bash launch_galyleo_singularity.sh
#
# Launches a JupyterLab session inside a Singularity container on the Expanse shared partition with:
#   1 node, 4 CPUs, 16 GB memory, 30 minute time limit
#   Account: sdp173
#   Singularity container: datascience-notebook_latest.sif
#
# Uncomment --reservation and --qos during the Summer Institute (Aug 3-7), then comment them out after.

/cm/shared/apps/sdsc/galyleo/galyleo launch \
  --account sdp173 \
  --partition shared \
  --reservation si26cpu \
  --qos normal-eot \
  --cpus 4 \
  --memory 16 \
  --time-limit 00:30:00 \
  --env-modules singularitypro \
  --sif /expanse/lustre/scratch/$USER/temp_project/datascience-notebook_latest.sif \
  --bind /expanse,/scratch \
  --interface lab \
  --quiet
