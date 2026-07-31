# Python for HPC

SDSC Summer Institute 2026

Andrea Zonca

Friday, August 7 | 8:30 AM to 11:20 AM

Speaker cue: Begin at 8:30. Keep this slide visible while participants settle
and open the lesson repository.

---

# What you will be able to do

- Speed up a numerical loop with Numba and time it fairly.
- Choose threads or processes based on the kind of work.
- Scale a Python calculation from one node to multiple nodes with Dask.

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
- Recap and take-home material.

Speaker cue: AI practice and other deep dives stay out of the live path.
Acknowledge that some learners are new to every tool and others have prior
experience.

---

# 1 of 7 | Setup

- Time check: 8:30 AM.
- Goal: open Jupyter and verify the environment.
- We move on when most laptops show yellow.

Speaker cue: This is a section divider. Do not begin the Numba section until
most participants can import the four required packages.

---

# SETUP | Open the lesson

- In the repository, open folder 6.1_python_for_HPC.
- Run bash launch_galyleo_compute.sh. It creates or reuses the pythonhpc Conda environment.
- Keep one Jupyter terminal available.

Speaker cue: The launcher uses the SI26 production account, reservation, and
QOS. It reads `environment.yaml`; students do not need separate Conda commands.
Participants already have Expanse accounts from Preparation Day.

---

# SETUP | Run the import check

- In Jupyter, open the lesson README.md.
- Copy and run the four-package import cell.
- Yellow means imports work.
- Blue means a helper should stop by.

Speaker cue: The check imports NumPy, Numba, Dask, and distributed. Ask helpers
to circulate and prioritize blue notes.

---

# SETUP | Measure one change at a time

- Flow: Check answer -> Time current version -> Make one change -> Check answer and time again.

Speaker cue: Read the four boxes from left to right. Ask, "Which part of your
own Python workflow currently feels slow?" Then transition to the first
notebook.

---

# 2 of 7 | Numba

- Time check: 8:42 AM.
- Goal: speed up one slow numerical loop and time it fairly.
- Core file: `1_numba/0_basics.ipynb`.

Speaker cue: This is the early win. Stay in the basics notebook and leave the
other Numba notebooks for later.

---

# NUMBA | What @jit does

- Add @jit above a function to ask Numba to compile it.
- The first call compiles the function and returns an answer.
- Later calls reuse the compiled code.
- Check the answer, call once, then time later calls.

Speaker cue: Introduce only `@jit`. Historical decorator defaults and aliases
do not help students complete this lesson.

---

# NUMBA | Open this notebook

- Open folder 1_numba.
- Open 0_basics.ipynb.
- Run through "Compare with NumPy."
- Predict each timing before you run it.
- Stop at "Your turn."

Speaker cue: Keep this slide visible while learners work through the guided
cells. Run the original Python function before the compiled function.

---

# NUMBA | Pause and ask

- Did all three versions return the same value?
- Which timing includes compilation?
- Why do we call the function once before timing it?

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

- First call: compile and run.
- Later calls: reuse the compiled code.
- @jit can speed up supported numerical loops.
- Time check: 9:15 AM.

Speaker cue: Ask, "When is a clear NumPy expression already good enough?" Close
the notebook only after learners can explain why the first call is not timed.

---

# 3 of 7 | Threads and processes

- Time check: 9:15 AM.
- Goal: predict the useful execution model.
- Notebook: threads versus processes.

Speaker cue: The goal is a decision rule, not a claim that one scheduler is
always faster.

---

# THREADS OR PROCESSES | Mental model

- Threads share one process and its memory.
- The GIL is a CPython rule: one thread runs Python code at a time.
- Processes can run Python code on separate CPU cores.
- Starting processes and sending data takes time and memory.

Speaker cue: Define the GIL before using the acronym. Keep the comparison to
four workers. Explain that the notebook's `scheduler=` setting selects threads
or processes.

---

# THREADS OR PROCESSES | Open this notebook

- Open folder 2_threads_vs_processes.
- Open threads_vs_processes.ipynb.
- Read the mental model.
- Predict both comparisons before running them.
- Stop at "Your turn."

Speaker cue: Keep this slide visible. The prediction is more important than the
exact timing on one node.

---

# THREADS OR PROCESSES | Pause and ask

- Which workload spends its time calculating in Python?
- Which workload mostly waits?
- What data would be expensive to send to a process?

Speaker cue: Pause near 9:27 and explicitly invite questions before the paired
activity.

---

# THREADS OR PROCESSES | Hands-on

- Run threads and processes with four workers.
- Explain each result with the mental model.
- Discuss one surprise with a neighbor.
- 12 minutes. Blue means help. Yellow means ready.

Speaker cue: 12 minutes. Discuss with a neighbor. Ask pairs to focus on the
reason, not on declaring a universal winner.

---

# THREADS OR PROCESSES | Debrief

- Python calculations often favor processes.
- Waiting work often favors threads.
- Shared data can change the tradeoff.
- Time check: 9:40 AM.

Speaker cue: Invite one pair to share a surprise. Then ask what evidence they
would collect for their own workload.

---

# 4 of 7 | Break

- Time check: 9:40 AM.
- Break ends at 9:50 AM.
- The Dask section starts after the break.

Speaker cue: Give everyone the full break. Keep cluster setup for its own block
later in the session.

---

# 5 of 7 | Dask tasks and chunks

- Time check: 9:50 AM.
- Goal: build a graph, then choose useful chunks.
- Notebooks: delayed, then multicore array.

Speaker cue: Dask delayed comes first. Move to arrays only after learners can
describe a task graph.

---

# DASK | Build a plan before running

- A task is one piece of work.
- A task graph is a plan showing tasks and their order.
- The scheduler assigns ready tasks to workers.
- compute() starts the work and returns the result.

Speaker cue: Use the file-processing story. A file count is one task. The final
summary waits for all file counts. The scheduler assigns work to workers.

---

# DASK | Open the delayed notebook

- Open folder 3_dask.
- Open 1_delayed.ipynb.
- Run through "Delay calls, then compute once."
- Inspect what exists before compute().
- Stop at "Your turn."

Speaker cue: Keep this slide visible while participants run the guided cells.
Avoid walking through every library call.

---

# DASK | Final summary and debrief

- Put the final summary inside the task graph.
- Compute only the final summary.
- 5 minutes. Blue means help. Yellow means ready.
- Then explain what compute() changed.

Speaker cue: Pause near 10:02 and invite questions. Debrief the graph before
opening the array notebook.

---

# DASK | Chunks are units of work

- Too small: Dask manages too many tiny tasks.
- Too large: a chunk may not fit or share work evenly.
- Useful chunks fit in memory and keep workers busy.
- Inspect chunks before compute().

Speaker cue: Connect chunk shape to both scheduling and memory. There is no
single best chunk size for every calculation.

---

# DASK | Open the array notebook

- In folder 3_dask, open 2_multicore_array.ipynb.
- Run through "Choose chunks."
- Compare the NumPy result with the Dask plan.
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
- Time check: 10:20 AM.

Speaker cue: Ask why both a tiny chunk and a huge chunk can be poor choices.
Close both notebooks before cluster setup.

---

# CLUSTER SETUP | 10 minutes

- In both terminals, cd 6.1_python_for_HPC.
- In a Jupyter terminal, run bash dask_slurm/launch_scheduler.sh.
- In a login terminal, run sbatch dask_slurm/dask_workers.slrm.
- Save the job number. Wait for two workers.

Speaker cue: Start at 10:20. Keep both terminals visible. The worker script has
a 30-minute limit and uses the SI26 production reservation and QOS. Helpers
should circulate during setup.

---

# 6 of 7 | Multi-node capstone

- Time check: 10:30 AM.
- Goal: run one Dask expression on two worker nodes.
- Notebook: multi-node distributed array.

Speaker cue: Limit every participant to the provided two-node worker job.
Cancel it as soon as the result is verified.

---

# CAPSTONE | Three roles

- Flow: Notebook asks for a result -> Scheduler assigns ready tasks -> Workers on node 1 and node 2 run tasks and hold chunks.
- The array expression does not change.

Speaker cue: Read the diagram from left to right. Ask learners to identify the
physical node used by each role.

---

# CAPSTONE | Open this notebook

- Open folder 3_dask.
- Open 4_multinode_distributed_array.ipynb.
- Run "Start the cluster."
- Open the Dask dashboard and confirm two worker hosts.
- Stop before "Build an array across the workers."

Speaker cue: Keep this slide visible. If workers do not connect promptly, move
that learner to the instructor cluster.

---

# CAPSTONE | Run and verify

- Build and calculate the array across both workers.
- Read worker hosts, threads, and result.
- Confirm the expected value.
- 18 minutes. Blue means help. Yellow means ready.

Speaker cue: 18 minutes. Clean up before moving on. Pause near 10:46 and invite
questions after workers connect. The evidence must show two distinct worker
hosts.

---

# CAPSTONE | Debrief and clean up

- What changed when we added nodes?
- What stayed the same in the Python expression?
- Cancel the worker job and stop the scheduler.
- Time check: 11:02 AM.

Speaker cue: Require cleanup before moving on. Ask for `squeue -u "$USER"` as
evidence that the worker job is gone.

---

# 7 of 7 | Recap

- Time check: 11:02 AM.
- Goal: choose the smallest useful layer.
- Final questions end at 11:20 AM.

Speaker cue: Return to the performance workflow and ask learners to map one of
their own workloads.

---

# RECAP | Decision map

- Slow numerical loop: Numba.
- Waiting tasks: threads or delayed.
- Python calculations: processes.
- Chunked or multi-node array: Dask.

Speaker cue: Check the answer and time the current version before making a
choice. Add nodes only after the one-node version works.

---

# RECAP | What you take home

- Core notebooks and optional practice notebooks.
- Production SI26 SLURM and Galyleo templates.
- A debug-queue validation workflow.
- Time check: 11:20 AM. Questions?

Speaker cue: Point to the directory READMEs and optional deep dives. Remind
everyone to confirm that no worker jobs remain. End here unless recap and
questions finish early.

---

# OPTIONAL | AI-assisted workflow

- Use only if recap and questions end early.
- Goal: test whether a suggestion is correct and useful.
- Otherwise, this section is take-home material.

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

- Open folder 4_ai_code_assist.
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
- Run the answer check and time the result twice.
- 8 minutes. Accept, revise, or reject.

Speaker cue: Give eight minutes. Put blue and yellow note meanings into words.
At four minutes, ask learners whether the suggestion changed the problem.

---

# AI | Debrief

- Plausible output is not evidence.
- Generated SLURM needs a line-by-line resource review.
- Keep only a verified improvement.
- Optional section. Stop when needed.

Speaker cue: Ask, "Which part of the answer must you verify before submitting a
job?" Invite at least one rejection or revision example.
