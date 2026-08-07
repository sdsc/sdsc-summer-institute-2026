#!/bin/bash
# Stage the pythonhpc conda env onto node-local SSD and activate it.
# Source this script per node, then run python from the staged env.
#
#   source 0_python_condaenv_scratch/stage_condaenv.sh pythonhpc
#
# On the first run it builds the env from environment.yaml and caches a
# conda-pack archive in $GALYLEO_CACHE_DIR so every later job (including
# launch_galyleo_compute.sh) stages it via Galyleo's --cache without rebuilding.
#
# Must be sourced, not executed, so the environment persists in the caller.

(return 0 2>/dev/null)
if [[ $? -ne 0 ]]; then
  echo "ERROR: this script must be sourced, not executed."
  echo "Usage: source ${BASH_SOURCE[0]} <conda_env_name>"
  exit 1
fi

if [[ -z "$1" ]]; then
  echo "ERROR: missing conda environment name."
  echo "Usage: source ${BASH_SOURCE[0]} <conda_env_name>"
  return 1
fi

ENV_NAME="$1"
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
GALYLEO_CACHE_DIR="${GALYLEO_CACHE_DIR:-${HOME}/.galyleo}"
LOCAL_SCRATCH_DIR="${SLURM_TMPDIR:-/tmp}"
CONDA_INSTALL_PATH="${LOCAL_SCRATCH_DIR}/${USER}_miniforge3"
ENV_ARCHIVE="${GALYLEO_CACHE_DIR}/${ENV_NAME}/${ENV_NAME}.tar.gz"
CONDA_PKGS_DIRS="${CONDA_INSTALL_PATH}/pkgs"

# --- One-time build + cache if needed ---
if [[ ! -f "$ENV_ARCHIVE" ]]; then
  echo "No cached archive at $ENV_ARCHIVE; building ${ENV_NAME} env once..."
  mkdir -p "$GALYLEO_CACHE_DIR/$ENV_NAME"
  export CONDA_PKGS_DIRS
  # Let conda and per-package post-install builds use every available core.
  ALLOCATED_CPUS="${SLURM_CPUS_PER_TASK:-$(nproc)}"
  export OMP_NUM_THREADS="$ALLOCATED_CPUS"
  export MKL_NUM_THREADS="$ALLOCATED_CPUS"
  export OPENBLAS_NUM_THREADS="$ALLOCATED_CPUS"
  echo "Using ${ALLOCATED_CPUS} cores for env build..."

  cd "$LOCAL_SCRATCH_DIR"
  if [[ ! -f Miniforge3-Linux-x86_64.sh ]]; then
    wget -q https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
  fi
  bash Miniforge3-Linux-x86_64.sh -b -p "$CONDA_INSTALL_PATH" >/dev/null
  source "$CONDA_INSTALL_PATH/etc/profile.d/conda.sh"
  conda activate base

  echo "Creating ${ENV_NAME} env from environment.yaml..."
  conda env create -p "${LOCAL_SCRATCH_DIR}/${ENV_NAME}" -f "${SCRIPT_DIR}/environment.yaml"

  echo "Packing ${ENV_NAME} env..."
  conda install -y -n base conda-pack -c conda-forge >/dev/null
  conda-pack -p "${LOCAL_SCRATCH_DIR}/${ENV_NAME}" -o "${LOCAL_SCRATCH_DIR}/${ENV_NAME}.tar.gz"
  if [[ ! -f "${LOCAL_SCRATCH_DIR}/${ENV_NAME}.tar.gz" ]]; then
    echo "ERROR: conda-pack failed to produce ${ENV_NAME}.tar.gz"
    return 1
  fi

  cp "${LOCAL_SCRATCH_DIR}/${ENV_NAME}.tar.gz" "$ENV_ARCHIVE"
  cp "${SCRIPT_DIR}/environment.yaml" "${GALYLEO_CACHE_DIR}/${ENV_NAME}/"
  ( cd "${GALYLEO_CACHE_DIR}/${ENV_NAME}" && md5sum environment.yaml > "${ENV_NAME}.md5" )
  rm -rf "${LOCAL_SCRATCH_DIR}/${ENV_NAME}" "${LOCAL_SCRATCH_DIR}/${ENV_NAME}.tar.gz"
  echo "Cached ${ENV_ARCHIVE}"
fi

# --- Stage the cached archive onto node-local SSD and activate ---
cd "$LOCAL_SCRATCH_DIR"
if [[ ! -d "${LOCAL_SCRATCH_DIR}/${ENV_NAME}/bin" ]]; then
  echo "Staging ${ENV_NAME} from cache..."
  rm -rf "$ENV_NAME"
  mkdir -p "$ENV_NAME"
  tar -xzf "$ENV_ARCHIVE" -C "$ENV_NAME"
fi
# conda's activate script references CONDA_PREFIX before it is set; run it
# without nounset so a parent shell's `set -u` cannot break activation.
set +u
source "${LOCAL_SCRATCH_DIR}/${ENV_NAME}/bin/activate"
if command -v conda-unpack >/dev/null 2>&1; then
  conda-unpack >/dev/null
fi
set -u 2>/dev/null || true

echo "Activated ${ENV_NAME} from ${LOCAL_SCRATCH_DIR}/${ENV_NAME}"
