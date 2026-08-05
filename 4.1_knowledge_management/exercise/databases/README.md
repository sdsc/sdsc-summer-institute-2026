## 1. Submit The Database Job

Load Slurm and run the launcher:

```bash
module load slurm
bash launch_kg_db.sh
```

The launcher creates the `logs` directory, generates a Neo4j password, and
submits `kg-db.sbatch`. The batch job uses the shared container images at:

```text
/expanse/lustre/projects/sdp173/zliang7/containers/weaviate.sif
/expanse/lustre/projects/sdp173/zliang7/containers/neo4j.sif
```

Slurm prints a job id:

```text
Submitted batch job (job id)
```

Check the queue:

```bash
squeue -u $USER
```

Wait until your `kg-db` job is running with state `R`.

## 2. Read The Database Job Log

Replace `<jobid>` with your actual job id:

```bash
cat logs/kg-db-<jobid>.out
```

Look for output like this:

```text
Put this in .env from Expanse Jupyter:
OPENAI_API_KEY=sk-v9OPgaiAitIXCwJG3IqDF8CnFN4wNkVd
OPENAI_MODEL=qwen3
WEAVIATE_HTTP_HOST=exp-3-29
WEAVIATE_HTTP_PORT=11105
WEAVIATE_GRPC_HOST=exp-3-29
WEAVIATE_GRPC_PORT=11106
WEAVIATE_COLLECTION=OcrChunk
NEO4J_URI=bolt://exp-3-29:11108
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=1566aec24e460b05701bf6b6
```

Keep this output. You will paste it into `.env` after Jupyter starts.

## 3. Start Jupyter From The Expanse Portal

Go back to the Expanse portal and click **Jupyter**.

Use these settings:

```text
Account: sdp173
Partition: shared
Time: 180
Cores: 2
Memory: 16
Jupyter interface: lab
Environment modules: cpu/0.17.3b,gcc/10.2.0,py-jupyterlab/3.2.1/fbrlmmt
```

## 4. Create The `.env` File In Jupyter

Inside JupyterLab, open **Terminal**.

Run:

```bash
cd "$PROJECT_DIR"
nano .env
```

Paste the values printed by your database job log.

Example:

```env
OPENAI_API_KEY=sk-your-real-key
OPENAI_MODEL=gpt-4.1-mini

WEAVIATE_HTTP_HOST=exp-3-29
WEAVIATE_HTTP_PORT=11105
WEAVIATE_GRPC_HOST=exp-3-29
WEAVIATE_GRPC_PORT=11106
WEAVIATE_COLLECTION=OcrChunk

NEO4J_URI=bolt://exp-3-29:11108
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=1566aec24e460b05701bf6b6
```

Replace:

- `OPENAI_API_KEY` with your real OpenAI API key.
- The node, ports, and Neo4j password with the values from your own Slurm log.

Save in `nano`:

```text
Ctrl+O
Enter
Ctrl+X
```

The notebook reads `.env` from the project root: `$PROJECT_DIR/.env`.

## 11. Install Python Dependencies In Jupyter

From the Jupyter terminal:

```bash
cd "$PROJECT_DIR"
python -m ensurepip --user || true
python -m pip install --user --upgrade pip
python -m pip install --user -r requirements.txt
```

If `python -m pip` says `No module named pip`, bootstrap pip:

```bash
cd "$PROJECT_DIR"
curl -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py --user
python -m pip install --user -r requirements.txt
```
