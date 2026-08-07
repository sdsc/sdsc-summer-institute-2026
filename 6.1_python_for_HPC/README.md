### SDSC Summer Institute 2026

# Session 6.1: Python for HPC

**Date:** Friday, August 7, 2026

**Time:** 8:30 AM to 11:20 AM Pacific
**Presented by:** [Andrea Zonca](https://www.sdsc.edu/research/experts/zonca_andrea.html)

Python can run faster and use more than one CPU or node when you choose the
right tool for the slow part. This notebook-first session follows one practical
path:

1. Measure a slow Python loop and speed it up with Numba.
2. Choose threads or processes based on the kind of work.
3. Divide work and arrays into smaller pieces with Dask.
4. Run the same Dask calculation on two Expanse nodes.

The supporting slides coordinate the session. They identify the file to open,
mark where to stop, display each timed activity, prompt the debrief, and
introduce the next section. Keep the current slide visible while working in a
notebook. The notebooks contain the executable explanations and code.

Presentation:

- [Google Slides deck](https://docs.google.com/presentation/d/1-aMB0CObn17n5KSDIbXWiiAnl5nN6rg5q4ni8lYor0U/edit?usp=sharing)
- [PDF copy](Python_for_HPC_SI26.pdf)

## Learning objectives

By the end of the session, you will be able to:

1. Find a slow numerical loop, speed it up with Numba, and time it fairly.
2. Choose threads or processes based on whether the work is calculating or
   waiting and whether it shares large data.
3. Choose a useful Dask chunk size and run the same calculation on one or two
   Expanse nodes.

## Prerequisites

You should be able to write a Python function and `for` loop, read a traceback,
and recognize a NumPy array. You also need:

- Your Expanse account, with login tested during Preparation Day.
- A browser for JupyterLab and a terminal connected to Expanse.
- The blue and yellow sticky notes distributed at the start of the session.

This session uses `sbatch`, `squeue`, and `scancel`, which were introduced in
the earlier Expanse jobs session. The slides show every command needed here.

Some participants will have used these tools before and others will be seeing
them for the first time. Both are expected. The core path is designed for a
first encounter, and optional deep dives are clearly labeled.

## Start here

From the repository root on Expanse:

```bash
cd 6.1_python_for_HPC
bash launch_galyleo_compute.sh
```

`launch_galyleo_compute.sh` launches JupyterLab with the `pythonhpc` conda
env (defined in `environment.yaml`). The env is staged to node-local scratch
via Galyleo's cache, so it is built once and reused on every session. To
regenerate it from scratch, remove the cached copy
(`rm -rf ~/.galyleo/pythonhpc`) or rebuild with
`0_python_condaenv_scratch/stage_condaenv.sh`.

The production launcher requests the SI26 account, CPU reservation, and
education QOS. It is intended for the institute. Instructors testing before the
event should follow [TESTING.md](TESTING.md) and use only the debug queue.

When JupyterLab opens, verify the environment:

```python
import socket
import numpy
import numba
import dask
import distributed

print(socket.gethostname())
print("NumPy", numpy.__version__)
print("Numba", numba.__version__)
print("Dask", dask.__version__)
print("Distributed", distributed.__version__)
```

If the imports work, put up the yellow sticky note. If you are stuck, put up
the blue sticky note so a helper can come to you.

## Core path

| Time | Activity | Material |
| --- | --- | --- |
| 8:30 to 8:42 | Setup, goals, and a simple performance workflow | Slides 1 to 8 and this README |
| 8:42 to 9:15 | Numba early win and hands-on exercise | Slides 9 to 14 and [`1_numba/0_basics.ipynb`](1_numba/0_basics.ipynb) |
| 9:15 to 9:40 | Threads, processes, and predict-then-check exercise | Slides 15 to 20 and [`2_threads_vs_processes/threads_vs_processes.ipynb`](2_threads_vs_processes/threads_vs_processes.ipynb) |
| 9:40 to 9:50 | Break | Slide 21 |
| 9:50 to 10:20 | Dask tasks, chunks, and hands-on exercise | Slides 22 to 29, [`3_dask/1_delayed.ipynb`](3_dask/1_delayed.ipynb), then [`3_dask/2_multicore_array.ipynb`](3_dask/2_multicore_array.ipynb) |
| 10:20 to 10:30 | Cluster setup | Slide 30 and [`dask_slurm/README.md`](dask_slurm/README.md) |
| 10:30 to 11:02 | Multi-node capstone | Slides 31 to 35 and [`3_dask/4_multinode_distributed_array.ipynb`](3_dask/4_multinode_distributed_array.ipynb) |
| 11:02 to 11:20 | Decision map, take-home files, and questions | Slides 36 to 38 |

The agenda allocates 170 minutes from 8:30 AM to 11:20 AM. The blocks above
total exactly 170 minutes, including the 10-minute break. The hands-on
activities reserve 57 minutes, or about 34% of the full session. Exercise
timing is part of the plan, not optional padding. Each section divider in the
deck shows the clock time the class should reach it.

## Optional deep dives

These files are for early finishers and post-session study:

- Slides 39 to 43 and [`4_ai_code_assist/README.md`](4_ai_code_assist/README.md):
  a short AI-assisted review exercise. Use this optional appendix only if the
  recap ends early; otherwise it is take-home material.
- [`1_numba/1_numpy.ipynb`](1_numba/1_numpy.ipynb): how Numba handles different
  NumPy array types and custom array functions.
- [`1_numba/2_threads.ipynb`](1_numba/2_threads.ipynb): use several threads
  inside one Numba function.
- [`1_numba/3_numba_groupby_pixels.ipynb`](1_numba/3_numba_groupby_pixels.ipynb):
  an authentic astronomy group-by optimization.
- [`3_dask/0_dask_graphs.ipynb`](3_dask/0_dask_graphs.ipynb): inspect task
  graphs in more detail.
- [`3_dask/3_multicore_array_outofcore.ipynb`](3_dask/3_multicore_array_outofcore.ipynb):
  reason about arrays larger than memory without performing a long classroom
  computation.

Not completing a deep dive is not falling behind.

## Folder guide

- [`1_numba/`](1_numba/README.md): single-core and threaded compilation.
- [`2_threads_vs_processes/`](2_threads_vs_processes/README.md): the GIL and
  scheduler choice.
- [`3_dask/`](3_dask/README.md): delayed tasks, arrays, chunking, and the
  multi-node capstone.
- [`4_ai_code_assist/`](4_ai_code_assist/README.md): optional practice using an
  AI assistant while retaining responsibility for resource requests and
  validation.
- [`0_python_condaenv_scratch/`](0_python_condaenv_scratch/README.md):
  conda environment staging scripts. Students do not open this folder during
  class.
- [`dask_slurm/`](dask_slurm/README.md): production SI26 scheduler and worker
  instructions.
- [`support/`](support/README.md): an optional container workflow. Students do
  not open this folder during class.
- [`INSTRUCTOR_GUIDE.md`](INSTRUCTOR_GUIDE.md): pacing, helper cues, and
  recovery options.
- [`TESTING.md`](TESTING.md): debug-queue validation procedure.
- [`VALIDATION.md`](VALIDATION.md): latest Expanse test results.

## A simple performance workflow

Start by timing the current program and checking that its answer is correct.
Then ask one question at a time:

1. Is most of the time spent in a numerical Python loop? Try Numba.
2. Does each piece of work mostly wait for a file or network response? Try
   threads or `dask.delayed`.
3. Does each piece spend most of its time calculating in Python? Try processes.
   Remember that sending data to another process also takes time and memory.
4. Is the array too large to calculate all at once with NumPy? Divide it into
   Dask chunks.
5. Is one node not enough? Add worker nodes only after the one-node version
   gives the right answer and has been timed.

Faster code is not automatically better code. Verify the answer, report the
resources used, and compare its time with the current version.
