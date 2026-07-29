#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"
mkdir -p logs

DB_PASSWORD="${DB_PASSWORD:-$(openssl rand -hex 12)}"

sbatch --export=ALL,DB_PASSWORD="$DB_PASSWORD" kg-db.sbatch
