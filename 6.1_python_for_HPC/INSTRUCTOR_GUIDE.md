# Instructor guide

This guide turns the session README into a delivery plan. It follows the Summer
Institute teaching guide: depth over breadth, an early win, explicit hands-on
time, regular question opportunities, and clear separation of core and optional
material.

## Before the session

- Launch and execute every core notebook on Expanse.
- Confirm the `pythonhpc` Galyleo cache exists and imports all packages in
  `environment.yaml`.
- Confirm the production scripts contain account `sdp173`, reservation
  `si26cpu`, and compute QOS `normal-eot`.
- Do not submit production scripts during testing. Use [TESTING.md](TESTING.md).
- Start one scheduler and worker cluster as a rehearsal.
- Brief one staff helper and the assigned intern. Both should know the core
  path, the Dask setup, and the recovery options below.
- Place one blue and one yellow sticky note at every seat.

## Room language

Open with:

> Some of you have optimized Python before, and for others this will be brand
> new. Both are expected. Focus on the decision process, not on memorizing
> syntax.

During exercises:

- Blue means "I am stuck or need help."
- Yellow means "I am ready to continue."
- Ask helpers to approach blue notes first and circulate continuously.
- Ask for questions at every transition. Allow a few seconds of silence.
- Frame errors as useful evidence about the program or environment.

## Detailed run of show

The native deck is the clock and navigation source for the room. Leave each
"Open this notebook" or exercise slide visible while participants work. Advance
only after the corresponding debrief slide. Section dividers show the target
clock time, so helpers and the instructor can make the same pacing decision.
Do not introduce a new term, file, command, or classroom task unless the current
slide introduces it in plain language.

### 8:30 to 8:42: Setup and map

- Show slides 1 through 8.
- Explain that the launcher reads `environment.yaml` and creates or reuses the
  `pythonhpc` Conda environment. Students do not run separate Conda commands.
- Ask participants to run the four-package import check.
- Do not begin the Numba demo until most laptops show yellow.
- Name the three learning objectives and the core versus deep-dive distinction.

Question prompt: "Which part of your own Python workflow currently feels slow?"

### 8:42 to 9:15: Numba

- Use slides 9 through 14.
- Use only `3_numba/0_basics.ipynb` in the core presentation.
- Run and time the original Python version before the compiled version.
- Introduce only `@jit`. Do not discuss old decorator defaults or aliases.
- Explain that the first call compiles and runs the function. Later calls reuse
  the compiled code, so time those later calls.
- Pause near 8:55 for questions before starting the hands-on portion.
- Give 12 minutes for the sum-of-squares exercise.
- At minute 9, ask for sticky-note status and announce three minutes remaining.
- Debrief correctness first, then performance.

Question prompt: "When is a clear NumPy expression already good enough?"

### 9:15 to 9:40: Threads and processes

- Use slides 15 through 20.
- Ask participants to predict both outcomes before timing either choice.
- Use four workers even on a 128-core node. The purpose is to reveal the
  execution model, not saturate the machine.
- Pause near 9:27 for questions before comparing the schedulers.
- Give 12 minutes for the predict-then-check activity.
- Explain that starting processes and sending them data takes time and memory.

Question prompt: "What data would be expensive to send to another process?"

### 9:40 to 9:50: Break

- Use slide 21.
- Give everyone the full break.
- Keep cluster setup for the next block so no learner must choose between
  resting and completing a core activity.

### 9:50 to 10:20: Dask tasks and chunks

- Use slides 22 through 29.
- Use the file-processing story in `1_delayed.ipynb`.
- Move to `2_multicore_array.ipynb` only after learners can describe a task
  graph.
- Pause near 10:02 for questions when moving from delayed tasks to arrays.
- Give 5 minutes for the delayed final summary and 10 minutes for chunk choice.
- Ask learners to explain why a very small chunk and a very large chunk can
  both be poor choices.

Question prompt: "What must Dask know before it can schedule the work?"

### 10:20 to 10:30: Cluster setup

- Use slide 30.
- Start the scheduler, then submit the worker job.
- Wait for two workers before opening the capstone notebook.
- Move anyone whose workers do not connect promptly to the instructor cluster.

### 10:30 to 11:02: Multi-node capstone

- Use slides 31 through 35.
- Use at most two worker nodes per participant. The job has a 30-minute limit,
  and learners cancel it as soon as they verify the result.
- Show `client.scheduler_info()` before the array computation.
- Ask participants to identify where the notebook, scheduler, and workers run.
- Pause near 10:46 for questions after workers connect and before computation.
- Give 18 minutes for setup and execution.
- Cancel worker jobs promptly after the result is verified.

Question prompt: "What changed in the Python expression when we added nodes?"

### 11:02 to 11:20: Recap

- Use slides 36 through 38.
- Return to the performance decision map.
- Ask participants to choose one take-home file.
- Invite final questions and point to the optional deep dives.

### Optional appendix: AI-assisted workflow

- Use slides 39 through 43 only if the recap ends early. Otherwise assign the
  section as take-home material.
- Use the short workflow in `2_ai_code_assist/README.md`.
- AI may suggest an individual command or review a small function.
- AI should not write the entire exercise solution.
- Require participants to inspect resource requests and run the provided tests.
- Give 8 minutes for the prompt-and-review exercise.

Question prompt: "Which part of this answer must you verify before submitting a
job?"

## Recovery options

If Galyleo startup is slow:

- Pair participants at one working notebook.
- Demonstrate from the instructor session while helpers continue setup.

If Numba compilation fails:

- Read the first typing error together.
- Compare the function with the supported NumPy subset.
- Continue with the provided solution only after discussing the cause.

If Dask workers do not connect:

- Check that the scheduler file exists.
- Check the worker job with `squeue -u "$USER"`.
- Read the worker output file.
- Use the instructor cluster for the capstone demo.
- Do not spend more than ten classroom minutes debugging individual clusters.

If time is short:

1. Keep the Numba exercise.
2. Keep the threads-versus-processes prediction.
3. Demonstrate the Dask capstone from the instructor cluster.
4. End with the recap and assign the optional appendix as take-home material.

Do not accelerate through concepts to preserve every notebook.
