#!/bin/bash
# SDSC Summer Institute 2026 -- Python for HPC: Interactive JupyterLab on compute partition
# Usage: bash launch_galyleo_compute.sh
#
# Launches a JupyterLab session on the Expanse compute partition with:
#   1 node, 128 CPUs, 242 GB memory, 4 hour time limit
#   Account: sdp173
#   Conda environment from environment.yaml (cached via conda-pack)

NOTEBOOK_FOLDER=$(pwd -P)  # Use current folder as the notebook working directory

galyleo launch \
  --account sdp173 \              # Slurm account for the Summer Institute allocation
  --partition compute \           # Expanse compute partition
  --cpus 128 \                    # 128 CPUs for the interactive session
  --memory 242 \                  # 242 GB memory (in GB)
  --time-limit 04:00:00 \         # 4 hour time limit
  --conda-yml environment.yaml \  # Conda environment definition file
  --notebook-dir ${NOTEBOOK_FOLDER} \  # Working directory for JupyterLab
  --interface lab \               # Use JupyterLab interface (options: lab, notebook, voila)
  --cache \                       # Cache conda environment using conda-pack for faster restarts
  --quiet                         # Suppress non-essential output
