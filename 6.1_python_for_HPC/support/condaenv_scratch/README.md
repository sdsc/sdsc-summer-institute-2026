# Conda env batch example

This directory contains the production two-node batch example and a node
diagnostic. Both use the shared `pythonhpc` conda env installed on project
storage by `../../setup_python_env.sh`.

## Files

- `python_expanse.slurm`: production SI26 two-node batch example. Runs
  `node_info.py` on each node using the shared conda env.
- `node_info.py`: prints the node, rank, CPU, memory, and environment path.

## Production use during SI26

From this directory:

```bash
sbatch python_expanse.slurm
squeue -u "$USER"
```

The script includes account `sdp173`, reservation `si26cpu`, and QOS
`normal-eot`. It requests two compute nodes for five minutes.

## Instructor testing

Do not submit the production script while validating the lesson. Follow
[`../../TESTING.md`](../../TESTING.md), request the debug queue directly, and
run `tests/run_debug_one_node.sh` inside that allocation.
