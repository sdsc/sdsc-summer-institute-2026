#!/bin/bash

#SBATCH --job-name=kg-db

#SBATCH --partition=shared

#SBATCH --nodes=1

#SBATCH --ntasks=1

#SBATCH --cpus-per-task=4

#SBATCH --mem=16G

#SBATCH --time=03:00:00

#SBATCH --account=sdp173

#SBATCH --output=logs/kg-db-%j.out



set -euo pipefail



module purge

module load cpu

module load slurm

module load singularitypro



ROOT="$SLURM_SUBMIT_DIR"

JOBDIR="/scratch/$USER/job_$SLURM_JOB_ID/kg-db"



mkdir -p "$ROOT/logs"

mkdir -p "$JOBDIR/weaviate"

mkdir -p "$JOBDIR/neo4j/data"

mkdir -p "$JOBDIR/neo4j/logs"



BASE=$((10000 + (SLURM_JOB_ID % 10000) * 5))

WEAVIATE_HTTP_PORT=$BASE

WEAVIATE_GRPC_PORT=$((BASE + 1))

NEO4J_HTTP_PORT=$((BASE + 2))

NEO4J_BOLT_PORT=$((BASE + 3))



DB_PASSWORD="${DB_PASSWORD:-please-change-me}"

unset NEO4J_PASSWORD



cleanup() {

  kill "${WEAVIATE_PID:-}" "${NEO4J_PID:-}" 2>/dev/null || true

  singularity instance stop "weaviate-$SLURM_JOB_ID" || true

  singularity instance stop "neo4j-$SLURM_JOB_ID" || true

}

trap cleanup EXIT



echo "Starting database services for job $SLURM_JOB_ID"

echo "NODE=$SLURMD_NODENAME"

echo "Runtime data directory: $JOBDIR"



test -f "$ROOT/images/weaviate_1.38.1.sif"

test -f "$ROOT/images/neo4j_2026.05.0.sif"



export SINGULARITYENV_QUERY_DEFAULTS_LIMIT=25

export SINGULARITYENV_AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true

export SINGULARITYENV_PERSISTENCE_DATA_PATH=/var/lib/weaviate

export SINGULARITYENV_ENABLE_API_BASED_MODULES=true

export SINGULARITYENV_CLUSTER_HOSTNAME=node1

export SINGULARITYENV_GRPC_PORT="$WEAVIATE_GRPC_PORT"



singularity instance start --cleanenv --writable-tmpfs --bind "$JOBDIR/weaviate:/var/lib/weaviate" "$ROOT/images/weaviate_1.38.1.sif" "weaviate-$SLURM_JOB_ID"



singularity exec --cleanenv instance://weaviate-$SLURM_JOB_ID /bin/weaviate --host 0.0.0.0 --port "$WEAVIATE_HTTP_PORT" --scheme http > "$JOBDIR/weaviate.log" 2>&1 &

WEAVIATE_PID=$!



export SINGULARITYENV_NEO4J_AUTH="neo4j/$DB_PASSWORD"

export SINGULARITYENV_NEO4J_dbms_security_auth__minimum__password__length=8

export SINGULARITYENV_NEO4J_server_http_listen__address="0.0.0.0:$NEO4J_HTTP_PORT"

export SINGULARITYENV_NEO4J_server_bolt_listen__address="0.0.0.0:$NEO4J_BOLT_PORT"

export SINGULARITYENV_NEO4J_server_http_advertised__address="$SLURMD_NODENAME:$NEO4J_HTTP_PORT"

export SINGULARITYENV_NEO4J_server_bolt_advertised__address="$SLURMD_NODENAME:$NEO4J_BOLT_PORT"



singularity instance start --cleanenv --writable-tmpfs --bind "$JOBDIR/neo4j/data:/data,$JOBDIR/neo4j/logs:/logs" "$ROOT/images/neo4j_2026.05.0.sif" "neo4j-$SLURM_JOB_ID"



singularity exec --cleanenv instance://neo4j-$SLURM_JOB_ID /startup/docker-entrypoint.sh neo4j > "$JOBDIR/neo4j.log" 2>&1 &

NEO4J_PID=$!



echo "Waiting for ports..."

for i in $(seq 1 90); do

  if ss -ltn | grep -q ":$WEAVIATE_HTTP_PORT " && ss -ltn | grep -q ":$NEO4J_BOLT_PORT "; then

    break

  fi



  if ! kill -0 "$WEAVIATE_PID" 2>/dev/null; then

    echo "Weaviate exited early:"

    cat "$JOBDIR/weaviate.log"

    exit 1

  fi



  if ! kill -0 "$NEO4J_PID" 2>/dev/null; then

    echo "Neo4j exited early:"

    cat "$JOBDIR/neo4j.log"

    exit 1

  fi



  sleep 2

done



ss -ltn | grep -E "$WEAVIATE_HTTP_PORT|$WEAVIATE_GRPC_PORT|$NEO4J_HTTP_PORT|$NEO4J_BOLT_PORT" || true



echo ""

echo "Put this in notebooks/.env from Expanse Jupyter:"

echo "OPENAI_API_KEY=sk-your-key-here"

echo "OPENAI_MODEL=gpt-4.1-mini"

echo "WEAVIATE_HTTP_HOST=$SLURMD_NODENAME"

echo "WEAVIATE_HTTP_PORT=$WEAVIATE_HTTP_PORT"

echo "WEAVIATE_GRPC_HOST=$SLURMD_NODENAME"

echo "WEAVIATE_GRPC_PORT=$WEAVIATE_GRPC_PORT"

echo "WEAVIATE_COLLECTION=OcrChunk"

echo "NEO4J_URI=bolt://$SLURMD_NODENAME:$NEO4J_BOLT_PORT"

echo "NEO4J_USERNAME=neo4j"

echo "NEO4J_PASSWORD=$DB_PASSWORD"



echo ""

echo "Logs:"

echo "$JOBDIR/weaviate.log"

echo "$JOBDIR/neo4j.log"



while kill -0 "$WEAVIATE_PID" 2>/dev/null && kill -0 "$NEO4J_PID" 2>/dev/null; do

  sleep 60

done



echo "One database process exited."

cat "$JOBDIR/weaviate.log" || true

cat "$JOBDIR/neo4j.log" || true

exit 1
