# Dask workers on Expanse

The multi-node capstone uses three roles:

```text
Jupyter notebook
      |
      v
Dask scheduler on the Jupyter node
      |
      +-----------------------+
      v                       v
worker on compute node 1   worker on compute node 2
```

The notebook asks for a result. The scheduler keeps track of what must run and
assigns ready tasks. Workers store chunks and perform those tasks.

## Production SI26 settings

`dask_workers.slrm` follows the CPU `srun` settings on repository `main`:

- Account: `sdp173`
- Partition: `compute`
- Reservation: `si26cpu`
- QOS: `normal-eot`
- Nodes: 2
- One worker per node
- 128 threads and 242 GB requested per node
- 30-minute limit, with immediate cancellation after the result is verified

Workers run inside the SI26 Singularity image at
`/expanse/lustre/projects/sds166/zonca/dask-numba-si26.sif` by default.
Override the path with `PYHPC_SIF_PATH` to test a different image.

These are production institute settings. Instructors testing before the event
must not submit this script. Use [`../TESTING.md`](../TESTING.md) and the debug
queue.

## 1. Start the scheduler

Open a terminal inside JupyterLab so the scheduler runs on the same node as the
notebook:

```bash
cd 6.1_python_for_HPC
bash dask_slurm/launch_scheduler.sh
```

Leave the terminal open. The scheduler writes its connection information to:

```text
~/.dask_scheduler.json
```

The home directory is visible from the worker nodes, so they can use the same
file.

## 2. Submit workers

From an Expanse login-node terminal:

```bash
cd 6.1_python_for_HPC
sbatch dask_slurm/dask_workers.slrm
squeue -u "$USER"
```

Save the job number printed by `sbatch`. You will use it to stop the workers.

Submit the script from any working directory. It resolves its supporting files
relative to the script location.

Within a minute or two, the scheduler terminal should report two workers. If it
does not:

```bash
squeue -u "$USER"
ls -1 dask-workers.*.out
```

Read the newest output file for the first error.

## 3. Connect from the notebook

Open `3_dask/4_multinode_distributed_array.ipynb`. Its connection cell reads
`~/.dask_scheduler.json`, waits for both workers, and prints worker hosts,
addresses, and thread counts.

The dashboard is available through Jupyter Server Proxy at:

```text
/proxy/8787/status
```

## 4. Stop everything

From the login node:

```bash
scancel <worker_job_id>
```

In the scheduler terminal, press `Ctrl-C`.

Confirm the job is gone:

```bash
squeue -u "$USER"
```

Removing stale scheduler state before a new run is safe:

```bash
rm -f "$HOME/.dask_scheduler.json"
```

Do not leave worker jobs running after the capstone.
