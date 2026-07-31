# Python for HPC

SDSC Summer Institute 2026

Andrea Zonca

Friday, August 7 | 8:30 AM to 11:20 AM

Speaker cue: Begin at 8:30. Keep this slide visible while participants settle
and open the lesson repository.

---

# What you will be able to do

- Compile and benchmark a numerical loop with Numba.
- Choose threads or processes from workload evidence.
- Choose Dask chunks and scale one expression across nodes.

Speaker cue: State these as decisions learners will make, not libraries they
must memorize.

---

# The slides lead the session

- Follow the file or action shown here.
- Work in the notebook while this slide stays visible.
- Return here for the debrief and next step.
- Blue means stuck. Yellow means ready.

Speaker cue: Explain that learners do not need to search for the next file.
Questions are welcome at every transition.

---

# Today has one core path

- Setup and performance workflow.
- Numba, then threads and processes.
- Dask on one node, then two nodes.
- AI review, recap, and take-home material.

Speaker cue: Optional deep dives stay out of the live path. Acknowledge that
some learners are new to every tool and others have prior experience.

---

# 1 of 8 | Setup

- Time check: 8:30 AM.
- Goal: open Jupyter and verify the environment.
- We move on when most laptops show yellow.

Speaker cue: This is a section divider. Do not begin the Numba section until
most participants can import the four required packages.

---

# SETUP | Open the lesson

- In the repository, open folder 6.1_python_for_HPC.
- Run bash launch_galyleo_compute.sh.
- Keep one Jupyter terminal available.

Speaker cue: The launcher uses the SI26 production account, reservation, and
QOS. Participants already have Expanse accounts from Preparation Day.

---

# SETUP | Run the import check

- In Jupyter, open the lesson README.md.
- Copy and run the four-package import cell.
- Yellow means imports work.
- Blue means a helper should stop by.

Speaker cue: The check imports NumPy, Numba, Dask, and distributed. Ask helpers
to circulate and prioritize blue notes.

---

# SETUP | Start with evidence

- Verify the answer.
- Time or profile a baseline.
- Change one layer at a time.
- Verify again and compare steady-state cost.

Speaker cue: Ask, "Which part of your own Python workflow currently feels
slow?" Then transition to the first notebook.

---

# 2 of 8 | Numba

- Time check: 8:42 AM.
- Goal: compile one hot loop and benchmark fairly.
- Core file: `3_numba/0_basics.ipynb`.

Speaker cue: This is the early win. Stay in the basics notebook and leave the
other Numba notebooks for later.

---

# NUMBA | jit and njit today

- Since Numba 0.59, bare @jit uses nopython mode.
- @njit is the explicit alias for @jit(nopython=True).
- This lesson uses @njit to make the intent visible.
- The first call compiles an input signature.

Speaker cue: The two decorators now have the same default compilation mode.
Keep `njit` in the lesson because it communicates the intended mode directly.

---

# NUMBA | Open this notebook

- Open folder 3_numba.
- Open 0_basics.ipynb.
- Run through "Compare with vectorized NumPy."
- Predict each timing before you run it.
- Stop at "Your turn."

Speaker cue: Keep this slide visible while learners work through the guided
cells. Run the Python baseline before the compiled function.

---

# NUMBA | Pause and ask

- Did all three versions return the same value?
- Which timing includes compilation?
- Why do we warm up before benchmarking?

Speaker cue: Pause near 8:55 and explicitly invite questions. Correctness comes
before the speed comparison.

---

# NUMBA | Hands-on

- Complete sum_of_squares.
- Check the result against NumPy.
- Warm up, then time both versions.
- 12 minutes. Blue means help. Yellow means ready.

Speaker cue: At minute 9, read the sticky notes and announce three minutes
remaining. Helpers should guide learners without typing the solution.

---

# NUMBA | Debrief

- First call: compilation plus execution.
- Later calls: steady-state execution.
- @njit helps supported numerical loops.
- Time check: 9:15 AM.

Speaker cue: Ask, "When would vectorized NumPy be preferable to Numba?" Close
the notebook only after learners can explain the warm-up.

---

# 3 of 8 | Threads and processes

- Time check: 9:15 AM.
- Goal: predict the useful execution model.
- Notebook: threads versus processes.

Speaker cue: The goal is a decision rule, not a claim that one scheduler is
always faster.

---

# SCHEDULERS | Mental model

- Threads share memory and one interpreter.
- The GIL limits simultaneous pure-Python bytecode.
- Processes use separate interpreters and memory.
- Startup and serialization have a cost.

Speaker cue: Define the GIL before using the acronym. Keep the comparison to
four workers.

---

# SCHEDULERS | Open this notebook

- Open folder 4_threads_vs_processes.
- Open threads_vs_processes.ipynb.
- Read the mental model.
- Predict both comparisons before running them.
- Stop at "Your turn."

Speaker cue: Keep this slide visible. The prediction is more important than the
exact timing on one node.

---

# SCHEDULERS | Pause and ask

- Which workload is CPU-bound pure Python?
- Which workload mostly waits?
- What data would be expensive to send to a process?

Speaker cue: Pause near 9:27 and explicitly invite questions before the paired
activity.

---

# SCHEDULERS | Hands-on

- Run both schedulers with four workers.
- Explain each result with the mental model.
- Discuss one surprise with a neighbor.
- 12 minutes. Blue means help. Yellow means ready.

Speaker cue: 12 minutes. Discuss with a neighbor. Ask pairs to focus on the
reason, not on declaring a universal winner.

---

# SCHEDULERS | Debrief

- CPU-bound Python often favors processes.
- Waiting work often favors threads.
- Shared data can change the tradeoff.
- Time check: 9:40 AM.

Speaker cue: Invite one pair to share a surprise. Then ask what evidence they
would collect for their own workload.

---

# 4 of 8 | Dask tasks and chunks

- Time check: 9:40 AM.
- Goal: build a graph, then choose useful chunks.
- Notebooks: delayed, then multicore array.

Speaker cue: Dask delayed comes first. Move to arrays only after learners can
describe a task graph.

---

# DASK | Graph before execution

- Delayed calls build tasks.
- Dependencies form a directed acyclic graph.
- The scheduler decides when and where tasks run.
- compute() triggers execution.

Speaker cue: Use the file-processing story. Define task, dependency, and
scheduler in plain language.

---

# DASK | Open the delayed notebook

- Open folder 5_dask.
- Open 1_delayed.ipynb.
- Run through "Delay calls, then compute once."
- Inspect what exists before compute().
- Stop at "Your turn."

Speaker cue: Keep this slide visible while participants run the guided cells.
Avoid walking through every library call.

---

# DASK | Delayed exercise and debrief

- Put the reduction inside the graph.
- Compute only the final summary.
- 5 minutes. Blue means help. Yellow means ready.
- Then explain what compute() changed.

Speaker cue: Pause near 9:52 and invite questions. Debrief the graph before
opening the array notebook.

---

# DASK | Chunks are units of work

- Too small: scheduling overhead dominates.
- Too large: memory pressure and weak parallelism.
- Useful chunks fit memory and keep workers busy.
- Inspect chunks before compute().

Speaker cue: Connect chunk shape to both scheduling and memory. There is no
single best chunk size for every calculation.

---

# DASK | Open the array notebook

- In folder 5_dask, open 2_multicore_array.ipynb.
- Run through "Choose chunks."
- Compare the eager and lazy objects.
- Stop at "Your turn."

Speaker cue: Keep this slide visible. Ask learners to name what has and has not
run before the final computation.

---

# DASK | Chunk exercise

- Try chunk sides 250, 1000, and 3000.
- Keep the mathematical expression unchanged.
- Compare task count, memory, and timing.
- 10 minutes. Blue means help. Yellow means ready.

Speaker cue: Ask learners to predict both extremes before running them.

---

# DASK | Debrief

- A graph is a plan, not a result.
- Chunks control scheduling and memory.
- NumPy can still win for small in-memory work.
- Time check: 10:10 AM.

Speaker cue: Ask why both a tiny chunk and a huge chunk can be poor choices.
Close both notebooks before the break.

---

# 5 of 8 | Break and cluster setup

- Time check: 10:10 AM.
- Break ends at 10:20 AM.
- Helpers can start cluster setup with ready learners.

Speaker cue: Anyone who needs the full break can watch the capstone demo and
still meet the learning objectives.

---

# CLUSTER SETUP | Two terminals

- In a Jupyter terminal, open folder dask_slurm.
- Run bash launch_scheduler.sh.
- In a login terminal, run sbatch dask_workers.slrm.
- Wait until the scheduler reports two workers.

Speaker cue: Keep both terminals visible. The worker script uses the SI26
production reservation and QOS. Helpers should circulate during setup.

---

# 6 of 8 | Multi-node capstone

- Time check: 10:20 AM.
- Goal: run one Dask expression on two worker nodes.
- Notebook: multi-node distributed array.

Speaker cue: Limit every participant to the provided two-node, ten-minute
worker job.

---

# CAPSTONE | Three roles

- Notebook builds the graph and requests a result.
- Scheduler tracks dependencies and assigns tasks.
- Workers hold chunks and execute tasks.
- The array expression does not change.

Speaker cue: Ask learners to identify the physical node used by each role.

---

# CAPSTONE | Open this notebook

- Open folder 5_dask.
- Open 4_multinode_distributed_array.ipynb.
- Run "Start the cluster."
- Confirm two distinct worker hosts.
- Stop before "Build a distributed array."

Speaker cue: Keep this slide visible. If workers do not connect promptly, move
that learner to the instructor cluster.

---

# CAPSTONE | Run and verify

- Build and compute the distributed array.
- Read worker hosts, threads, and result.
- Confirm the expected value.
- 18 minutes. Blue means help. Yellow means ready.

Speaker cue: 18 minutes. Clean up before moving on. Pause near 10:36 and invite
questions after workers connect. The evidence must show two distinct worker
hosts.

---

# CAPSTONE | Debrief and clean up

- What changed when we added nodes?
- What stayed the same in the Python expression?
- Cancel the worker job and stop the scheduler.
- Time check: 10:52 AM.

Speaker cue: Require cleanup before moving on. Ask for `squeue -u "$USER"` as
evidence that the worker job is gone.

---

# 7 of 8 | AI-assisted workflow

- Time check: 10:52 AM.
- Goal: turn a suggestion into a tested hypothesis.
- Page: AI code-assist README.

Speaker cue: Learners may use an approved assistant for one command or function,
not for the entire exercise solution.

---

# AI | A reviewable loop

- State the environment, limits, and correct result.
- Ask for one small change and an explanation.
- Inspect commands and resource requests.
- Test correctness, then performance.

Speaker cue: An assistant cannot know whether a resource request is appropriate
or whether a scientific result is valid.

---

# AI | Open this page

- Open folder 2_ai_code_assist.
- Open README.md.
- Read "A useful HPC prompt."
- Choose one function from the Numba notebook.
- Stop at "Hands-on: ask, inspect, test."

Speaker cue: Participants without an approved assistant can review the supplied
prompt and checklist with a partner.

---

# AI | Ask, inspect, test

- Ask for one Numba optimization.
- Identify every package and resource assumption.
- Run the correctness check and benchmark twice.
- 8 minutes. Accept, revise, or reject.

Speaker cue: Give eight minutes. Put blue and yellow note meanings into words.
At four minutes, ask learners whether the suggestion changed the problem.

---

# AI | Debrief

- Plausible output is not evidence.
- Generated SLURM needs a line-by-line resource review.
- Keep only a verified improvement.
- Time check: 11:08 AM.

Speaker cue: Ask, "Which part of the answer must you verify before submitting a
job?" Invite at least one rejection or revision example.

---

# 8 of 8 | Recap

- Time check: 11:08 AM.
- Goal: choose the smallest useful layer.
- Final questions end at 11:20 AM.

Speaker cue: Return to the performance workflow and ask learners to map one of
their own workloads.

---

# RECAP | Decision map

- Hot numerical loop: Numba.
- Waiting tasks: threads or delayed.
- CPU-bound Python: processes.
- Chunked or multi-node array: Dask.

Speaker cue: Profiling and correctness wrap every choice. Scaling out is the
last step, not the first.

---

# RECAP | What you take home

- Tested core and optional notebooks.
- Production SI26 SLURM and Galyleo templates.
- A debug-queue validation workflow.
- Time check: 11:20 AM. Questions?

Speaker cue: Point to the directory READMEs and optional deep dives. Remind
everyone to confirm that no worker jobs remain.
