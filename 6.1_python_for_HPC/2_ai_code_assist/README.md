# AI-assisted Python for HPC

An AI coding assistant can help explain a traceback, propose a small refactor,
or suggest a command. It cannot know whether a job request is appropriate for
your allocation, whether a numerical answer is scientifically valid, or whether
generated code scales well.

The goal of this activity is to practice a short, reviewable loop:

1. Give the assistant a small task and the constraints that matter.
2. Ask it to explain its proposed change.
3. Inspect every command and resource request.
4. Test correctness before measuring speed.
5. Compare against a baseline and keep only a verified improvement.

During the hands-on exercise, use AI for an individual command or function. Do
not ask it to write the entire exercise solution.

## Tools

You may use any assistant approved for your data and organization. Common
options include:

- [GitHub Copilot in VS Code](https://docs.github.com/en/copilot).
- [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli).
- [Gemini CLI](https://github.com/google-gemini/gemini-cli).

Availability, features, and pricing change. Follow the current official
documentation for installation and account requirements.

The safest default is to run the assistant on your laptop against a local clone,
then transfer reviewed code to Expanse. A terminal assistant can technically run
on a remote system when installed and permitted, but do not upload confidential
data, credentials, unpublished results, or restricted source code to a service
unless your project explicitly allows it.

## A useful HPC prompt

Good prompts include the execution environment, resource limit, correctness
condition, and the smallest requested change.

```text
This function runs on one Expanse CPU node with 4 CPUs and 16 GB of memory.
The input is a NumPy float64 array. Preserve the result within rtol=1e-12.
Suggest one Numba optimization for the loop below. Explain why Numba can
compile it, provide a correctness check, and provide a benchmark that excludes
first-call compilation. Do not add a GPU or a multi-node design.
```

This is more useful than "make this faster" because it prevents the assistant
from silently changing the problem or inventing resources.

## Hands-on: ask, inspect, test

Choose one function from `3_numba/0_basics.ipynb`.

1. Ask an assistant for one optimization using the prompt pattern above.
2. Before running the answer, identify:
   - The requested CPUs, memory, and partition.
   - Any package, network, or file-system assumptions.
   - The correctness test.
   - Whether the benchmark includes compilation or setup.
3. Run the correctness test.
4. Run the benchmark twice.
5. Decide whether to accept, revise, or reject the suggestion.

Put up the yellow sticky note when you can explain your decision. Put up the
blue sticky note if the proposed code or command is unclear.

## Review checklist for generated SLURM

Never submit generated SLURM without checking:

- `--account`, `--partition`, `--reservation`, and `--qos`.
- Node, task, CPU, GPU, memory, and time requests.
- Paths and environment activation.
- Input and output locations.
- Cleanup and cancellation commands.
- Whether the same test can run on the debug queue with smaller resources.

For SI26 production CPU scripts, the expected values are account `sdp173`,
reservation `si26cpu`, and QOS `normal-eot`. The debug queue test does not use
the reservation or QOS.

## Common failure patterns

- **Plausible but nonexistent flags:** confirm with `srun --help`, `sbatch
  --help`, or SDSC documentation.
- **Benchmarking compilation:** warm up Numba before timing.
- **Oversubscription:** do not let Dask, Numba, BLAS, and multiprocessing each
  create a full set of threads.
- **Changed numerical behavior:** compare arrays with an appropriate tolerance
  and inspect edge cases.
- **Unnecessary scale:** first make the one-node version correct and measured.
- **Unreviewed commands:** terminal assistants may propose commands that write,
  install, delete, or submit jobs. Read each command before approving it.

## A productive follow-up prompt

```text
Review your answer as an HPC instructor. List every assumption, identify any
oversubscription risk, and show the smallest debug-queue test that could
falsify the claimed speedup.
```

Treat the response as a hypothesis. Your test result is the evidence.
