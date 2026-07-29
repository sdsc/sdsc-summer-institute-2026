# Threads, processes, and the GIL

The core notebook is
[`threads_vs_processes.ipynb`](threads_vs_processes.ipynb).

It uses two predict-then-check comparisons:

1. Pure-Python CPU work, where processes can bypass the Global Interpreter
   Lock.
2. Waiting work, where threads can overlap without process startup and data
   transfer.

The notebook intentionally caps the worker count. A 128-core node does not make
128 tiny benchmark tasks pedagogically useful.

`workloads.py` contains importable benchmark functions so process-based
execution works consistently from Jupyter and automated notebook tests.

Before running each comparison, write down a prediction. The explanation is
more important than which timing is smaller on one particular run.
