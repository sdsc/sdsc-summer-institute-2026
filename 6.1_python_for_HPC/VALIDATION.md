# Validation record

## August 6, 2026

Validation was run directly against the live `pythonhpc` Conda environment on
the active galyleo compute node, after the environment was rebuilt with updated
package versions. This validated that all notebooks still work with the new
versions.

### Environment

- Node: `exp-1-29` (galyleo job `53050077`).
- Live Conda environment (`pythonhpc`): Python 3.12.13, NumPy 2.4.6, Numba
  0.66.0, Dask 2026.7.1, distributed 2026.7.1, pandas 3.0.5.
- Test runner: `tests/execute_local_notebooks.py` run with the live
  environment interpreter.

### One-node notebooks

All 9 notebooks that do not require a live cluster passed:

| Notebook | Seconds |
| --- | ---: |
| `1_numba/0_basics.ipynb` | 1.691 |
| `1_numba/1_numpy.ipynb` | 1.834 |
| `1_numba/2_threads.ipynb` | 1.860 |
| `1_numba/3_numba_groupby_pixels.ipynb` | 1.729 |
| `2_threads_vs_processes/threads_vs_processes.ipynb` | 9.044 |
| `3_dask/0_dask_graphs.ipynb` | 1.958 |
| `3_dask/1_delayed.ipynb` | 2.802 |
| `3_dask/2_multicore_array.ipynb` | 2.149 |
| `3_dask/3_multicore_array_outofcore.ipynb` | 1.815 |

### Multi-node capstone

`3_dask/4_multinode_distributed_array.ipynb` was executed end to end against a
live scheduler with two workers running on the same node (`exp-1-29`), using
Dask `dask-scheduler` and `dask-worker` from the live environment. The
distributed computation was verified correct (result 64,000,000), and the
client closed cleanly.

Only the notebook's "two distinct worker hosts" assertion could not be
exercised in this run, because both workers ran on the single node (the live
environment is node-local; no cached `pythonhpc.tar.gz` existed to stage a
second node). The two-node host wiring itself was validated previously (July
30, 2026) and is unaffected by the package version update.

### Notes

- The earlier galyleo rebuild log reported a `conda pack` failure
  (`conda: error: invalid choice: 'pack'`), so no `pythonhpc.tar.gz` was
  written to `~/.galyleo/pythonhpc/`. See VALIDATION for the follow-up on
  fixing the packing step.

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
| `1_numba/0_basics.ipynb` | 1.676 | 2.617 |
| `1_numba/1_numpy.ipynb` | 1.817 | 2.093 |
| `1_numba/2_threads.ipynb` | 1.820 | 1.895 |
| `1_numba/3_numba_groupby_pixels.ipynb` | 1.907 | 1.876 |
| `2_threads_vs_processes/threads_vs_processes.ipynb` | 9.295 | 9.009 |
| `3_dask/0_dask_graphs.ipynb` | 1.856 | 2.560 |
| `3_dask/1_delayed.ipynb` | 3.229 | 2.341 |
| `3_dask/2_multicore_array.ipynb` | 2.173 | 2.111 |
| `3_dask/3_multicore_array_outofcore.ipynb` | 1.819 | 1.901 |

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

### Schedule and deck refresh

The live path now ends with the recap on slides 36 through 38. The AI material
is an optional appendix on slides 39 through 43.

- The native Google Slides deck contains 43 slides in the intended order.
- All standard slide titles and bullets match `slides/SLIDES.md`.
- All 43 speaker-note pages match the source.
- The exported PDF contains 43 pages.
- The full-deck contact sheet and both native diagrams passed visual review.
- The worker-job limit is 30 minutes, which covers the 18-minute capstone
  exercise. Learners still cancel the job as soon as they verify the result.
- `python tests/validate_material.py`: passed after the refresh.

### Folder renumbering

The numbered folders now follow the teaching order: Numba, threads and
processes, Dask, then the optional AI appendix. Environment staging and the
optional container workflow moved under `support/`.

- Static material validation passed after the move.
- All local links in Markdown files and notebook text resolve.
- All old folder paths were removed from the lesson source and exported PDF.
