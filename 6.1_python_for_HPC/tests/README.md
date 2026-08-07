# Material validation scripts

- `validate_material.py`: checks notebook structure, required production SLURM
  settings, shell syntax, links, stale values, and prohibited em dash
  characters.
- `execute_local_notebooks.py`: executes every notebook that does not require a
  live distributed cluster.
- `run_debug_one_node.sh`: stages the `pythonhpc` environment, then executes
  all local notebooks.
- `run_debug_dask.sh`: validates a real scheduler, workers on multiple allocated
  debug nodes, and the capstone notebook.

Run these only from an Expanse debug allocation as documented in
[`../TESTING.md`](../TESTING.md).

Results are written to `../test-results/`, which is ignored by Git.
