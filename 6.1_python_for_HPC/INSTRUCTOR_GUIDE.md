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

### 8:30 to 8:42: Setup and map

- Show slides 1 through 4.
- Ask participants to run the four-package import check.
- Do not begin the Numba demo until most laptops show yellow.
- Name the three learning objectives and the core versus deep-dive distinction.

Question prompt: "Which part of your own Python workflow currently feels slow?"

### 8:42 to 9:15: Numba

- Use only `3_numba/0_basics.ipynb` in the core presentation.
- Run the uncompiled baseline before the compiled version.
- Explicitly separate first-call compilation from steady-state timing.
- Give 12 minutes for the sum-of-squares exercise.
- At minute 9, ask for sticky-note status and announce three minutes remaining.
- Debrief correctness first, then performance.

Question prompt: "When would vectorized NumPy be preferable to Numba?"

### 9:15 to 9:40: Threads and processes

- Ask participants to predict both outcomes before running either benchmark.
- Use at most eight workers even on a 128-core node. The purpose is to reveal
  the execution model, not saturate the machine.
- Give 12 minutes for the predict-then-check activity.
- Call out process startup and serialization overhead.

Question prompt: "What data would be expensive to send to another process?"

### 9:40 to 10:10: Dask tasks and chunks

- Use the file-processing story in `1_delayed.ipynb`.
- Move to `2_multicore_array.ipynb` only after learners can describe a task
  graph.
- Give 15 minutes for the chunk-choice exercise.
- Ask learners to explain why a very small chunk and a very large chunk can
  both be poor choices.

Question prompt: "What must Dask know before it can schedule the work?"

### 10:10 to 10:20: Break and cluster setup

- Helpers start the scheduler and worker setup with participants who want to run
  the capstone.
- Anyone who needs a break can watch the capstone demo without losing a core
  learning objective.

### 10:20 to 10:52: Multi-node capstone

- Use at most two worker nodes per participant and keep the job to ten minutes.
- Show `client.scheduler_info()` before the array computation.
- Ask participants to identify where the notebook, scheduler, and workers run.
- Give 18 minutes for setup and execution.
- Cancel worker jobs promptly after the result is verified.

Question prompt: "What changed in the Python expression when we added nodes?"

### 10:52 to 11:08: AI-assisted workflow

- Use the short workflow in `2_ai_code_assist/README.md`.
- AI may suggest an individual command or review a small function.
- AI should not write the entire exercise solution.
- Require participants to inspect resource requests and run the provided tests.
- Give 8 minutes for the prompt-and-review exercise.

Question prompt: "Which part of this answer must you verify before submitting a
job?"

### 11:08 to 11:20: Recap

- Return to the performance decision map.
- Ask participants to choose one take-home artifact.
- Invite final questions and point to the optional deep dives.

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
4. Assign AI and all deep dives as take-home material.

Do not accelerate through concepts to preserve every notebook.
