# Run a Python container on Expanse

This is an optional setup deep dive. The core session uses
`launch_galyleo_compute.sh` and `environment.yaml`.

The workflow demonstrates three HPC container habits:

1. Pull or build images on a compute node, not a login node.
2. Put temporary conversion files and caches on node-local SSD.
3. Store the final immutable `.sif` file on Lustre scratch or project storage.

## Instructor test on the debug queue

Do not use the production Galyleo launcher while testing. Request a debug node
without the SI26 reservation or QOS:

```bash
srun \
  --account=sds166 \
  --partition=debug \
  --nodes=1 \
  --ntasks=1 \
  --cpus-per-task=4 \
  --mem=16G \
  --time=00:30:00 \
  --pty bash
```

Inside the allocation:

```bash
module load singularitypro

export SINGULARITY_CACHEDIR="$SLURM_TMPDIR/singularity_cache"
export SINGULARITY_TMPDIR="$SLURM_TMPDIR"
mkdir -p "$SINGULARITY_CACHEDIR"
```

## Pull a demonstration image

Choose an immutable, project-approved image tag when reproducibility matters.
The `latest` tag below is convenient for a short demonstration, but it can
change and should not be treated as a reproducible research environment.

```bash
mkdir -p "/expanse/lustre/scratch/$USER/temp_project"

singularity pull \
  "/expanse/lustre/scratch/$USER/temp_project/datascience-notebook_latest.sif" \
  docker://jupyter/datascience-notebook:latest
```

Verify the image before launching Jupyter:

```bash
singularity exec \
  "/expanse/lustre/scratch/$USER/temp_project/datascience-notebook_latest.sif" \
  python -c 'import numpy; print(numpy.__version__)'
```

## Production SI26 launch

After the image has been verified:

```bash
bash launch_galyleo_singularity.sh
```

The launcher follows `srun-shared.sh` on repository `main`: account `sdp173`,
partition `shared`, reservation `si26cpu`, four CPUs, and 16 GB of memory. The
shared partition does not have a shared education QOS, so the launcher does not
set one.

Update the `.sif` path in the launcher if you stored the image elsewhere.

## Build the lesson-specific image

[`singularity_container/`](singularity_container/README.md) contains a recipe
for the packages used by this lesson. Building requires an environment that
supports unprivileged or administrator-assisted Singularity builds. The recipe
has a `%test` section that imports the core Python packages.

## Cleanup

The node-local cache disappears when the debug job ends. Remove any obsolete
large `.sif` files from Lustre when they are no longer needed.

See the [Galyleo documentation](https://hpc-training.sdsc.edu/galyleo/) for
launcher options.
