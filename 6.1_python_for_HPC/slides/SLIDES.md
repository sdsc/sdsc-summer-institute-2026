# Python for HPC

SDSC Summer Institute 2026
Andrea Zonca, SDSC

Speaker cue: Begin at 8:30. Keep the title slide visible during setup.

---

# What you will be able to do

- Compile and benchmark a numerical Python loop with Numba.
- Choose threads or processes by reasoning about the GIL and overhead.
- Choose Dask chunks and scale one expression from one node to multiple nodes.

Speaker cue: These are decisions learners should be able to make, not a list of
libraries to memorize.

---

# How today works

- Core path: one Numba exercise, one scheduler exercise, one Dask capstone.
- Deep dives are labeled optional and can be completed later.
- Blue sticky note: I am stuck or need help.
- Yellow sticky note: I am ready to continue.

Speaker cue: Ask learners to place a yellow note after the import check.

---

# Start with evidence

1. Verify the answer.
2. Profile or time a baseline.
3. Change one layer: compile, schedule, chunk, or distribute.
4. Verify again.
5. Compare steady-state time and resources.

Speaker cue: Faster output is not useful if the numerical answer changed.

---

# Numba: compile the hot loop

- `@njit` turns a supported Python function into machine code.
- The first call compiles a signature.
- Warm up before timing.
- Numba helps loops that do not vectorize cleanly.

Speaker cue: Open `3_numba/0_basics.ipynb`.

---

# Hands-on 1: benchmark fairly

- Complete `sum_of_squares`.
- Check it against NumPy.
- Warm up the compiled function.
- Time both implementations.
- Explain the result in one sentence.

12 minutes. Blue means help. Yellow means ready.

---

# Threads and processes

- Threads share memory and one CPython interpreter.
- The GIL limits simultaneous pure-Python bytecode.
- Processes have separate interpreters and memory.
- Data transfer and startup are not free.

Speaker cue: Ask for predictions before running the notebook.

---

# Hands-on 2: predict, then check

- CPU-bound pure Python: threads or processes?
- Waiting on I/O: threads or processes?
- Use at most eight workers.
- Explain any result that differs from your prediction.

12 minutes. Blue means help. Yellow means ready.

---

# Dask separates graph from execution

- Delayed functions create tasks.
- Dependencies form a directed acyclic graph.
- A scheduler decides when and where tasks run.
- `compute()` triggers execution.

Speaker cue: Use the file-processing example before arrays.

---

# Chunks are the unit of array work

- Too small: scheduling overhead dominates.
- Too large: poor parallelism and memory pressure.
- Useful chunks fit memory and keep workers busy.
- Inspect `.chunks`, `.numblocks`, and `.nbytes`.

Speaker cue: Open `5_dask/2_multicore_array.ipynb`.

---

# From one node to multiple nodes

- Notebook: builds the graph and requests the result.
- Scheduler: tracks dependencies and assigns tasks.
- Workers: hold chunks and execute tasks.
- The Dask array expression does not change.

Speaker cue: Draw the three roles and name their Expanse nodes.

---

# Capstone: run the cluster

1. Start the scheduler in the Jupyter terminal.
2. Submit the two-node worker job from the login node.
3. Connect with the scheduler file.
4. Verify workers, compute, then cancel the job.

18 minutes. Blue means help. Yellow means ready.

---

# AI is a hypothesis generator

- Provide environment, limits, and correctness criteria.
- Ask for one small change and an explanation.
- Inspect every command and resource request.
- Test correctness before performance.
- Keep only evidence-backed improvements.

Speaker cue: AI may help with one command or function, not the whole exercise.

---

# AI exercise: ask, inspect, test

- Ask for one Numba optimization.
- Identify resource and package assumptions.
- Check that compilation is excluded from timing.
- Run the correctness test and benchmark twice.
- Accept, revise, or reject the suggestion.

8 minutes. Be ready to explain your decision.

---

# Choose the smallest useful layer

- Hot numerical loop: Numba.
- Independent waiting tasks: threads or delayed.
- CPU-bound Python tasks: processes.
- Chunked array: Dask array.
- More than one node: distributed scheduler.

Speaker cue: Profiling and correctness wrap every choice.

---

# What you take home

- Tested notebooks with core and optional paths.
- Production SI26 SLURM and Galyleo templates.
- A debug-queue validation workflow.
- A repeatable AI review checklist.
- One decision map for the next slow Python program.

Speaker cue: Invite final questions and point to each directory README.
