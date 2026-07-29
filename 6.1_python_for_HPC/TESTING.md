# Testing on Expanse

This procedure is for instructors validating the material before the Summer
Institute. It intentionally uses the `debug` partition without the SI26
reservation or education QOS.

Do not submit `launch_galyleo_compute.sh`, `python_expanse.slurm`, or
`dask_workers.slrm` for this test. Those are production teaching scripts and
contain the institute reservation and QOS.

## One-node notebook validation

From the Expanse login node, request a short debug allocation:

```bash
srun \
  --account=sds166 \
  --partition=debug \
  --nodes=1 \
  --ntasks=1 \
  --cpus-per-task=4 \
  --mem=32G \
  --time=00:30:00 \
  --pty bash
```

Inside the allocation, activate a test environment and run:

```bash
cd /path/to/sdsc-summer-institute-2026/6.1_python_for_HPC
bash tests/run_debug_one_node.sh
```

The script stages the cached `pythonhpc` environment, runs every local core and
optional notebook, and repeats the suite inside the instructor's SI26
Singularity image. Set `PYHPC_SIF_PATH` first to use a different image. It skips
only the multi-node notebook, which requires a scheduler and workers and is
covered by the next test.

## Multi-node Dask validation

Request two debug nodes and launch the test as a step inside that allocation:

```bash
salloc \
  --account=sds166 \
  --partition=debug \
  --nodes=2 \
  --ntasks=2 \
  --ntasks-per-node=1 \
  --cpus-per-task=4 \
  --mem=16G \
  --time=00:30:00 \
  srun \
    --overlap \
    --cpu-bind=none \
    --nodes=1 \
    --ntasks=1 \
    bash -lc \
    'cd /path/to/6.1_python_for_HPC && source 0_python_condaenv_scratch/stage_condaenv.sh pythonhpc && bash tests/run_debug_dask.sh'
```

The test creates a temporary scheduler file, runs one worker on each allocated
node with explicit `srun` steps, executes the capstone computation, checks the
result, and stops all processes. It does not call the production SLURM script.

## Record the result

For each test, record:

- Git commit.
- Date and Expanse node names.
- Python, Numba, Dask, and distributed versions.
- Notebook pass or failure.
- Runtime and any warnings that learners will see.

The validation scripts write a machine-readable summary under
`test-results/`. That directory is ignored by Git.
