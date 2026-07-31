### SDSC Summer Institute 2026

# Session 6.1: Python for HPC

**Date:** Friday, August 7, 2026

**Time:** 8:30 AM to 11:20 AM Pacific
**Presented by:** [Andrea Zonca](https://www.sdsc.edu/research/experts/zonca_andrea.html)

Python can be fast, parallel, and distributed when you choose the right tool for
the bottleneck. This notebook-first session follows one practical path:

1. Measure a slow Python loop and compile it with Numba.
2. Choose threads or processes by reasoning about the Global Interpreter Lock.
3. Express work as Dask tasks and chunked arrays.
4. Run the same Dask computation across multiple Expanse nodes.

The [supporting slides](slides/README.md) coordinate the session. They identify
the file to open, mark where to stop, display each timed activity, prompt the
debrief, and introduce the next section. Keep the current slide visible while
working in a notebook. The notebooks contain the executable explanations and
code.

Presentation:

- [Google Slides deck](https://docs.google.com/presentation/d/1-aMB0CObn17n5KSDIbXWiiAnl5nN6rg5q4ni8lYor0U/edit?usp=sharing)
- [PDF copy](slides/Python_for_HPC_SI26.pdf)

## Learning objectives

By the end of the session, you will be able to:

1. Identify a hot loop, JIT-compile it with Numba, and benchmark the compiled
   result without including compilation time.
2. Choose threads or processes for a workload based on the GIL, data sharing,
   and task overhead.
3. Choose useful Dask chunks and scale a computation from one node to a small
   multi-node cluster on Expanse.

## Prerequisites

You should be able to write a Python function and `for` loop, read a traceback,
and recognize a NumPy array. You also need:

- Your Expanse account, with login tested during Preparation Day.
- A browser for JupyterLab and a terminal connected to Expanse.
- The blue and yellow sticky notes distributed at the start of the session.

Some participants will have used these tools before and others will be seeing
them for the first time. Both are expected. The core path is designed for a
first encounter, and optional deep dives are clearly labeled.

## Start here

From the repository root on Expanse:

```bash
cd 6.1_python_for_HPC
bash launch_galyleo_compute.sh
```

The production launcher requests the SI26 account, CPU reservation, and
education QOS. It is intended for the institute. Instructors testing before the
event should follow [TESTING.md](TESTING.md) and use only the debug queue.

When JupyterLab opens, verify the environment:

```python
import socket
import numpy
import numba
import dask

print(socket.gethostname())
print("NumPy", numpy.__version__)
print("Numba", numba.__version__)
print("Dask", dask.__version__)
```

If the imports work, put up the yellow sticky note. If you are stuck, put up
the blue sticky note so a helper can come to you.

## Core path

| Time | Activity | Material |
| --- | --- | --- |
| 8:30 to 8:42 | Setup, goals, and performance decision map | Slides 1 to 8 and this README |
| 8:42 to 9:15 | Numba early win and hands-on exercise | Slides 9 to 14 and [`3_numba/0_basics.ipynb`](3_numba/0_basics.ipynb) |
| 9:15 to 9:40 | Threads, processes, and predict-then-check exercise | Slides 15 to 20 and [`4_threads_vs_processes/threads_vs_processes.ipynb`](4_threads_vs_processes/threads_vs_processes.ipynb) |
| 9:40 to 10:10 | Dask tasks, chunks, and hands-on exercise | Slides 21 to 28, [`5_dask/1_delayed.ipynb`](5_dask/1_delayed.ipynb), then [`5_dask/2_multicore_array.ipynb`](5_dask/2_multicore_array.ipynb) |
| 10:10 to 10:20 | Break and cluster setup | Slides 29 to 30 and [`dask_slurm/README.md`](dask_slurm/README.md) |
| 10:20 to 10:52 | Multi-node capstone | Slides 31 to 35 and [`5_dask/4_multinode_distributed_array.ipynb`](5_dask/4_multinode_distributed_array.ipynb) |
| 10:52 to 11:08 | AI-assisted HPC workflow | Slides 36 to 40 and [`2_ai_code_assist/README.md`](2_ai_code_assist/README.md) |
| 11:08 to 11:20 | Decision map, take-home artifacts, and questions | Slides 41 to 43 |

The agenda allocates 170 minutes from 8:30 AM to 11:20 AM. The blocks above
total exactly 170 minutes, including the 10-minute break. The hands-on
activities reserve 65 minutes, or 38% of the full session. Exercise timing is
part of the plan, not optional padding. Each section divider in the deck shows
the clock time the class should reach it.

## Optional deep dives

These files are for early finishers and post-session study:

- [`3_numba/1_numpy.ipynb`](3_numba/1_numpy.ipynb): dtype specialization and
  custom ufuncs.
- [`3_numba/2_threads.ipynb`](3_numba/2_threads.ipynb): automatic Numba
  parallelization and `prange`.
- [`3_numba/3_numba_groupby_pixels.ipynb`](3_numba/3_numba_groupby_pixels.ipynb):
  an authentic astronomy group-by optimization.
- [`5_dask/0_dask_graphs.ipynb`](5_dask/0_dask_graphs.ipynb): inspect task
  graphs in more detail.
- [`5_dask/3_multicore_array_outofcore.ipynb`](5_dask/3_multicore_array_outofcore.ipynb):
  reason about arrays larger than memory without performing a long classroom
  computation.

Not completing a deep dive is not falling behind.

## Folder guide

- [`0_python_condaenv_scratch/`](0_python_condaenv_scratch/README.md): stage a
  cached Conda environment on compute-node local SSD.
- [`1_python_singularity/`](1_python_singularity/README.md): optional container
  workflow.
- [`2_ai_code_assist/`](2_ai_code_assist/README.md): use an AI assistant while
  retaining responsibility for resource requests and validation.
- [`3_numba/`](3_numba/README.md): single-core and threaded compilation.
- [`4_threads_vs_processes/`](4_threads_vs_processes/README.md): the GIL and
  scheduler choice.
- [`5_dask/`](5_dask/README.md): delayed tasks, arrays, chunking, and the
  multi-node capstone.
- [`dask_slurm/`](dask_slurm/README.md): production SI26 scheduler and worker
  instructions.
- [`slides/`](slides/README.md): Google Slides link, accessible source, PDF, and
  reference information.
- [`INSTRUCTOR_GUIDE.md`](INSTRUCTOR_GUIDE.md): pacing, helper cues, and
  recovery options.
- [`TESTING.md`](TESTING.md): debug-queue validation procedure.

## The performance decision map

Start with a profile and one question at a time:

1. Is the bottleneck a Python or NumPy loop that is hard to vectorize? Try
   Numba.
2. Are independent tasks waiting on files or network I/O? Try threads or
   `dask.delayed`.
3. Are pure-Python tasks CPU-bound? Try processes, while accounting for data
   serialization.
4. Is an array too large for one eager NumPy operation? Use Dask chunks.
5. Does the work exceed one node? Use a distributed scheduler only after the
   single-node version is correct and measured.

Faster code is not automatically better code. Verify the answer, report the
resources used, and compare against a measured baseline.
