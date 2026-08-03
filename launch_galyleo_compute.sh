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

/cm/shared/apps/sdsc/galyleo/galyleo launch \
  --account sdp173 \
  --partition compute \
  --reservation si26cpu \
  --qos normal-eot \
  --cpus 128 \
  --memory 242 \
  --time-limit 04:00:00 \
  --interface lab \
  --notebook-dir "${NOTEBOOK_FOLDER}" \
  --env-modules cpu/0.17.3b,gcc/10.2.0,py-jupyterlab/3.2.1 \
  --quiet
