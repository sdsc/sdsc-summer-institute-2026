### SDSC Summer Institute 2026
# Session 6.1 Python for HPC

**Date:** Friday, August 7, 2026

**Time:** 8:30 AM – 11:20 AM Pacific

**Summary**: In this session we will introduce 2 key technologies in the Python ecosystem that provide significant benefits for scientific applications run in supercomputing environments. Previous Python experience is recommended but not required.
* (1) First, we will learn how to speed up Python code compiling it on-the-fly with numba
* (2) Then we will introduce the threads, processes and the Global Interpreter lock and we will leverage first numba then dask to use all available cores on a machine
* (3) Finally we will distribute computations across multiple nodes launching dask workers on a separate Expanse job.

**Presented by:** [Andrea Zonca](https://www.sdsc.edu/research/experts/zonca_andrea.html)

### Prerequisites

* **Working knowledge of Python** — you can write a `for` loop, define a function, and read a traceback.
* **Familiarity with NumPy** — you understand `np.ndarray`, dtype, and broadcasting.
* An Expanse training account (set up on Preparation Day) and the ability to launch a Jupyter session on a compute node via `launch_galyleo.sh`.

If you are new to Python or NumPy, follow along with the demos — the hands-on exercises are optional and the take-home material works on its own.

### Learning objectives

By the end of this session you will be able to:

1. **JIT-compile a hot loop with Numba** — add one decorator to a pure-Python function and get a 10–100x speedup, and explain *why* it works (LLVM, `nopython` mode, and the GIL).
2. **Choose threads vs. processes** for a given workload by reasoning about the GIL, I/O-bound vs. CPU-bound code, and shared memory.
3. **Chunk a NumPy array with Dask** and scale the same computation from one core to many cores to multiple nodes, using the `dask_slurm/` scripts to launch workers on a separate Expanse job.

### Reading and Presentations:
* **Lecture material:**
   * [Introductory Slides on Google Docs](https://docs.google.com/presentation/d/1AW0-MrupxGU7XFfcrPN2YQyqxD_yDlh2akXg7L4_x6s/edit?usp=sharing)
* **Source Code/Examples:**
   See all the files in this folder and subfolders

## Folder structure

**Setup**
* `launch_galyleo_compute.sh` — launch the Jupyter environment on Expanse via [galyleo](https://github.com/mkandes/galyleo)
* `environment.yaml` — conda environment used by the notebooks
* `0_python_condaenv_scratch/` — stage a cached conda environment on the local SSD of compute nodes
* `1_python_singularity/` — build and launch a Singularity container with the Python environment
* `2_ai_code_assist/` — notes on using AI code assistants (Copilot, Copilot CLI) for Python development

**Notebooks (in order)**
* `3_numba/` — early win: speed up Python with one decorator (`@jit`), then `prange`, ufuncs, and a groupby exercise
* `4_threads_vs_processes/` — threads vs. processes and the GIL, with predict-then-check exercises
* `5_dask/` — Dask graphs, delayed, multi-core, out-of-core (optional), and the **multinode capstone**

**Dask cluster (for the multinode notebook)**
* `dask_slurm/` — SLURM scripts to launch Dask workers on a separate Expanse job

### Recommended flow

1. `3_numba/0_basics.ipynb` — the 50x speedup (early win)
2. `3_numba/3_numba_groupby_pixels.ipynb` — authentic astrophysics exercise
3. `4_threads_vs_processes/threads_vs_processes.ipynb` — why threads don't always help
4. `5_dask/0_dask_graphs.ipynb` → `1_delayed.ipynb` → `2_multicore_array.ipynb` — scale up on one node
5. `5_dask/4_multinode_distributed_array.ipynb` — **capstone**: distribute across Expanse nodes

`3_numba/1_numpy.ipynb`, `3_numba/2_threads.ipynb`, and `5_dask/3_multicore_array_outofcore.ipynb` are optional deep dives for participants who finish early.
