#!/bin/bash
# SDSC Summer Institute 2026 -- Python for HPC: Singularity container on shared partition
# Usage: bash launch_galyleo_singularity.sh
#
# Launches a JupyterLab session inside a Singularity container on the Expanse shared partition with:
#   1 node, 4 CPUs, 16 GB memory, 30 minute time limit
#   Account: sdp173
#   Singularity container: datascience-notebook_latest.sif

/cm/shared/apps/sdsc/galyleo/galyleo launch \
  --account sdp173 \              # Slurm account for the Summer Institute allocation
  --partition shared \            # Expanse shared partition
  --cpus 4 \                      # 4 CPUs for the interactive session
  --memory 16 \                   # 16 GB memory (in GB)
  --time-limit 00:30:00 \         # 30 minute time limit
  --env-modules singularitypro \  # Load the Singularity Pro environment module
  --sif /expanse/lustre/scratch/$USER/temp_project/datascience-notebook_latest.sif \  # Path to Singularity container image
  --bind /expanse,/scratch \      # Bind-mount /expanse and /scratch inside the container
  --interface lab \               # Use JupyterLab interface (options: lab, notebook, voila)
  --quiet                         # Suppress non-essential output
