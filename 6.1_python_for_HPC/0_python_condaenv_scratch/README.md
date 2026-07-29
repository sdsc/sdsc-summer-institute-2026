# Stage a Conda environment on local SSD

This optional workflow copies the cached `pythonhpc` environment from the
Galyleo cache into each compute node's local SSD. It demonstrates a common HPC
pattern: keep the authoritative environment on a shared file system, then stage
frequently accessed files onto node-local storage for a job.

This is an advanced setup example, not part of the core classroom path.

## Files

- `python_expanse.slurm`: production SI26 two-node batch example.
- `stage_condaenv.sh`: sourced once per node to install Miniforge and unpack the
  cached environment under `$SLURM_TMPDIR`.
- `node_info.py`: prints the node, rank, CPU, memory, and environment path.

## Prerequisite

Run `launch_galyleo_compute.sh` at least once with `--cache` so this archive
exists:

```text
~/.galyleo/pythonhpc/pythonhpc.tar.gz
```

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
[`../TESTING.md`](../TESTING.md), request the debug queue directly, and source
the staging script inside that allocation.

## Expected output

The SLURM output should contain two different hostnames, one task per node, and
an environment path under each node's `$SLURM_TMPDIR`.

The local environment disappears when the job ends. The cached archive in your
home directory remains.
