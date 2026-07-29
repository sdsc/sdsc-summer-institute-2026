# Python for HPC

SDSC Summer Institute 2026

Andrea Zonca

Friday, August 7 | 8:30 AM to 11:20 AM

Speaker cue: Begin at 8:30. Keep this slide visible while participants finish
the import check.

---

# What you will be able to do

- Compile and benchmark a numerical loop with Numba.
- Choose threads or processes from workload evidence.
- Choose Dask chunks and scale one expression across nodes.

Speaker cue: State these as decisions learners will make, not libraries they
must memorize.

---

# How today works

- Core path: Numba, scheduler choice, and a Dask capstone.
- Deep dives are optional and ready for later.
- Blue note means stuck. Yellow means ready.
- Questions are welcome at every transition.

Speaker cue: Ask learners to place a yellow note after the import check.
Acknowledge the range of prior experience.

---

# Start with evidence

- Verify the answer.
- Time or profile a baseline.
- Change one layer at a time.
- Verify again and compare steady-state cost.

Speaker cue: Faster output is not useful if the numerical answer changed. Open
the core Numba notebook.

---

# Numba compiles the hot loop

- `@njit` turns supported Python into machine code.
- The first call compiles a signature.
- Warm up before timing.
- Best target: a numerical loop that does not vectorize cleanly.

Speaker cue: Run the baseline first. Separate compilation time from steady-state
execution.

---

# Hands-on 1: benchmark fairly

- Complete `sum_of_squares`.
- Check the result against NumPy.
- Warm up the compiled function.
- Time both versions and explain the evidence.
- 12 minutes. Blue means help. Yellow means ready.

Speaker cue: At minute 9, read the sticky notes and announce three minutes
remaining. Debrief correctness before speed.

---

# Threads and processes

- Threads share memory and one interpreter.
- The GIL limits simultaneous pure-Python bytecode.
- Processes use separate interpreters and memory.
- Startup and serialization are real costs.

Speaker cue: Ask for predictions before running either benchmark. Use only four
workers.

---

# Hands-on 2: predict, then check

- Predict CPU-bound pure Python.
- Predict waiting work.
- Run both schedulers with four workers.
- Explain any result that surprises you.
- 12 minutes. Discuss with a neighbor.

Speaker cue: Ask what data would be expensive to send to another process.
Invite one pair to share a surprise.

---

# Dask separates graph from execution

- Delayed calls build tasks instead of running immediately.
- Dependencies form a directed acyclic graph.
- The scheduler decides when and where tasks run.
- `compute()` triggers execution.

Speaker cue: Use the file-processing example. Give five minutes for the delayed
reduction, then move to arrays.

---

# Chunks are the unit of array work

- Too small: scheduling overhead dominates.
- Too large: memory pressure and weak parallelism.
- Useful chunks fit memory and keep workers busy.
- Inspect chunks, blocks, and bytes before `compute()`.

Speaker cue: Give ten minutes for the chunk comparison. Ask why both extremes
can be poor choices.

---

# From one node to multiple nodes

- Notebook builds the graph and requests a result.
- Scheduler tracks dependencies and assigns tasks.
- Workers hold chunks and execute tasks.
- The Dask array expression stays the same.

Speaker cue: Name the physical node used by each role. Confirm two distinct
worker hosts. Emphasize that the Python expression does not change.

---

# Capstone: run the cluster

- Start the scheduler on the Jupyter node.
- Submit the worker job from a login terminal.
- Verify workers on distinct nodes.
- Compute, inspect evidence, then cancel the job.
- 18 minutes. Clean up before moving on.

Speaker cue: Helpers circulate during setup. If workers do not connect promptly,
use the instructor cluster.

---

# AI is a hypothesis generator

- Provide environment, limits, and correctness criteria.
- Ask for one small change and an explanation.
- Inspect commands and resource requests.
- Test correctness before performance.
- Keep only evidence-backed improvements.

Speaker cue: AI may help with one command or function, not the whole exercise.

---

# AI exercise: ask, inspect, test

- Ask for one Numba optimization.
- Find package and resource assumptions.
- Check that timing excludes compilation.
- Run correctness and benchmark tests.
- Accept, revise, or reject the suggestion.

Speaker cue: Give eight minutes. Participants without an approved assistant can
review the supplied prompt and checklist with a partner.

---

# Choose the smallest useful layer

- Hot numerical loop: Numba.
- Waiting tasks: threads or delayed.
- CPU-bound Python: processes.
- Chunked array: Dask array.
- More than one node: distributed scheduler.

Speaker cue: Profiling and correctness wrap every choice. Ask learners which
layer matches one of their workflows.

---

# What you take home

- Tested core and optional notebooks.
- Production SI26 SLURM and Galyleo templates.
- A debug-queue validation workflow.
- An AI review checklist.
- One decision map for your next slow program.

Speaker cue: Invite final questions. Point to the directory READMEs and remind
everyone to cancel worker jobs.
