# Dask notebooks

Dask builds a task graph and executes independent pieces of work with a chosen
scheduler. Dask arrays add NumPy-like operations over explicit chunks.

## Core path

1. [`1_delayed.ipynb`](1_delayed.ipynb): turn independent file operations into
   a task graph.
2. [`2_multicore_array.ipynb`](2_multicore_array.ipynb): choose chunks and use
   several cores on one node.
3. [`4_multinode_distributed_array.ipynb`](4_multinode_distributed_array.ipynb):
   connect the same array expression to workers on multiple Expanse nodes.

## Optional deep dives

- [`0_dask_graphs.ipynb`](0_dask_graphs.ipynb): inspect a task graph and see
  how chunk size changes its structure.
- [`3_multicore_array_outofcore.ipynb`](3_multicore_array_outofcore.ipynb):
  reason about virtual arrays larger than memory and compute a bounded slice.

## Chunk checklist

A useful chunk is:

- Small enough to fit comfortably in worker memory.
- Large enough that computation dominates scheduling overhead.
- Aligned with the way data is stored and accessed when possible.
- Numerous enough to keep workers busy, but not so numerous that the scheduler
  manages millions of tiny tasks.

Changing from NumPy to Dask does not guarantee a speedup. Build the graph, inspect
the chunks, compute once, and compare against a measured baseline.
