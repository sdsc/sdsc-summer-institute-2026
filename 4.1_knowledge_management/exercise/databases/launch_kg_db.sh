#!/bin/bash

set -euo pipefail

mkdir -p logs

DB_PASSWORD="${DB_PASSWORD:-$(openssl rand -hex 12)}"

sbatch --export=ALL,DB_PASSWORD="$DB_PASSWORD" kg-db.sbatch
