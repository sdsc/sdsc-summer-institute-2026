# Support files

Students do not need to open this folder during the live lesson.

- [`condaenv_scratch/`](condaenv_scratch/README.md) copies the prepared Python
  environment to each compute node. The `python_expanse.slurm` batch example uses
  this support code.
- [`python_singularity/`](python_singularity/README.md) builds the SI26
  Singularity image. Dask workers launched by `dask_workers.slrm` run inside
  this container.

The numbered folders in the lesson root follow the teaching order.
