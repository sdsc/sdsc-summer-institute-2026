# Conda environment staging

This folder stages the shared `pythonhpc` conda environment onto node-local
SSD and caches it across sessions, so the env is built exactly once.

## Files

- `stage_condaenv.sh`: source this per node to unpack the cached env onto
  node-local scratch and activate it. On the first run it builds `pythonhpc`
  from `../environment.yaml` and caches a conda-pack archive in
  `~/.galyleo/pythonhpc/`, which Galyleo then reuses on every launch.
- `python_expanse.slurm`: one-node, one-process job that creates and caches the
  env by sourcing `stage_condaenv.sh`. Run it once before the institute.
- `node_info.py`: prints the node, rank, CPU, memory, and environment path.

## Production use during SI26

From this directory, run it once to create and cache the env:

```bash
sbatch python_expanse.slurm
squeue -u "$USER"
```

The script includes account `sdp173`, reservation `si26cpu`, and QOS
`normal-eot`. It requests two compute nodes for five minutes.

## Notes

- `launch_galyleo_compute.sh` uses Galyleo's `--cache` against the same
  `~/.galyleo/pythonhpc/` archive, so it stages and reuses the env without
  building a second one.
- Remove the cached archive to force a clean rebuild:
  `rm -rf ~/.galyleo/pythonhpc`.

## Instructor testing

Do not submit the production script while validating the lesson. Follow
[`../TESTING.md`](../TESTING.md), request the debug queue directly, and
run `tests/run_debug_one_node.sh` inside that allocation.
