# Validation record

## July 30, 2026

The plain-language lesson review was tested from the PR branch
`import-python-hpc-2025`. The working tree was based on commit `aaf931b` and
included the uncommitted review changes described by the local diff.

### Static checks

- `python tests/validate_material.py`: passed.
- Notebook JSON: all 10 notebooks passed.
- Slide source: 43 slides.
- Exported PDF: 43 pages, with no clipped or overlapping text in the full-deck
  visual review.
- Removed terminology check: passed.

### One-node debug test

- Expanse job: `52732440`.
- Node: `exp-9-55`.
- Partition: `debug`.
- Resources: 1 node, 4 CPUs, 32 GB, 30-minute limit.
- Cached Conda environment: Python 3.12.11, NumPy 1.26.4, Numba 0.61.2, Dask
  2025.7.0, distributed 2025.7.0.
- SI26 Singularity image: Python 3.12.0, NumPy 2.4.6, Numba 0.65.1, Dask
  2026.6.0, distributed 2026.6.0.

All 9 notebooks that do not require a live cluster passed in both
environments:

| Notebook | Conda seconds | Container seconds |
| --- | ---: | ---: |
| `3_numba/0_basics.ipynb` | 1.676 | 2.617 |
| `3_numba/1_numpy.ipynb` | 1.817 | 2.093 |
| `3_numba/2_threads.ipynb` | 1.820 | 1.895 |
| `3_numba/3_numba_groupby_pixels.ipynb` | 1.907 | 1.876 |
| `4_threads_vs_processes/threads_vs_processes.ipynb` | 9.295 | 9.009 |
| `5_dask/0_dask_graphs.ipynb` | 1.856 | 2.560 |
| `5_dask/1_delayed.ipynb` | 3.229 | 2.341 |
| `5_dask/2_multicore_array.ipynb` | 2.173 | 2.111 |
| `5_dask/3_multicore_array_outofcore.ipynb` | 1.819 | 1.901 |

The container run printed warnings that the temporary validation kernels used
unencrypted local TCP connections. These warnings came from the notebook test
runner and did not cause failures.

### Two-node Dask debug test

- Expanse job: `52733082`.
- Nodes: `exp-9-55` and `exp-9-56`.
- Partition: `debug`.
- Resources: 2 nodes, one 4-thread worker per node, 16 GB per node,
  30-minute limit.
- Result: passed.
- Evidence: two workers connected from two distinct hosts, and the capstone
  notebook completed successfully.

The final worker and scheduler processes were stopped by the test cleanup. The
resulting SLURM step cancellation messages were expected, and no jobs remained
in the queue.
