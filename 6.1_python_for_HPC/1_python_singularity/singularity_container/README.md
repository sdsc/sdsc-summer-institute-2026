# Lesson-specific Singularity image

`Singularity.anaconda3-dask-numba` starts from the Ubuntu 22.04
`naked-singularity` image and creates a Python 3.12 environment named `si26`
with the notebook, Numba, Dask, and visualization packages used in this lesson.

## Build

The build host must support Singularity builds. Review the definition file, then
run:

```bash
make build
```

The recipe's `%test` section checks the Python version and imports NumPy, Numba,
Dask, distributed, pandas, psutil, and Graphviz.

## Copy to Expanse

```bash
make copy
```

The Makefile copies `dask-numba-si26.sif` to the lesson instructor's project
directory. Other users should change that destination.

Large `.sif` files are build artifacts and are not committed to this repository.
