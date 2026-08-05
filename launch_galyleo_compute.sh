#!/bin/bash
# SDSC Summer Institute 2026 -- Interactive JupyterLab on compute partition
# Usage: bash galyleo_compute.sh
#
# Launches a JupyterLab session on the Expanse compute partition with:
#   1 node, 128 CPUs, 242 GB memory, 4 hour time limit
#   Account: sdp173
#   Jupyterlab default modules
#
# The reservation and QOS are required for SI26 production sessions.

set -euo pipefail

NOTEBOOK_FOLDER=$(pwd -P)

galyleo_args=(
  --account sdp173                # Slurm account for the Summer Institute allocation
  --reservation si26cpu           # Summer Institute CPU reservation (remove after institute)
  --partition compute             # Expanse compute partition
  --qos normal-eot                # Education, outreach, and training QoS (remove after institute)
  --cpus 128                      # Total CPU cores for the session
  --memory 242                    # Memory in GB (leave headroom of 2 GB)
  --time-limit 04:00:00           # Maximum wall time for the session
  --interface lab                 # Launch JupyterLab (not notebook)
  --notebook-dir "${NOTEBOOK_FOLDER}"  # Working directory for notebooks
  --env-modules cpu/0.17.3b,gcc/10.2.0,py-jupyterlab/3.2.1  # Required environment modules
  --quiet                         # Suppress verbose output
)

/cm/shared/apps/sdsc/galyleo/galyleo launch "${galyleo_args[@]}"
