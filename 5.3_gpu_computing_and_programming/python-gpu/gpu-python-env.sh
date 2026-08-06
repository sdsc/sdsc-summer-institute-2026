#!/bin/bash

# GPU Python environment for SDSC Summer Institute 2026
# Source this file after obtaining an interactive Expanse GPU node.

module reset
module load gpu/0.21.2a
module load cuda12.2/toolkit
module load gcc/13.3.0
module load python/3.11.9

# Activate shared Python virtual environment
source /expanse/lustre/projects/sdp173/agoetz/gpu-python/bin/activate

echo "GPU Python environment loaded."
echo "Python: $(which python)"
python --version
