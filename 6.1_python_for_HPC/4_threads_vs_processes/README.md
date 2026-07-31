# Threads, processes, and the GIL

The core notebook is
[`threads_vs_processes.ipynb`](threads_vs_processes.ipynb).

It uses two predict-then-check comparisons:

1. Work that spends its time calculating in Python, where processes can run on
   separate CPU cores.
2. Waiting work, where threads can overlap without process startup and data
   transfer.

The notebook uses only four workers. Using all 128 CPU cores would make the
example harder to understand and would waste shared classroom resources.

`workloads.py` holds the two small example functions. Keeping them in a regular
Python file lets processes run them reliably from Jupyter and from the lesson
tests.

Before running each comparison, write down a prediction. The explanation is
more important than which timing is smaller on one particular run.
