Compiler vectorization
======================

This simple C program computes PI several times.

Build and test setup
--------------------

Start an interactive session with
srun --partition=shared --reservation=si26cpu --account=sdp173 --pty --nodes=1 --ntasks-per-node=1 --mem=8G -c 4 -t 00:30:00 /bin/bash
(Adapt partition/reservation/account if needed)

Then load the correct compiler
module load gcc/10.2.0

Let's build the code with 4 different compiler options
------------------------------------------------------
gcc -O3 -o pi_std pi.c -lm
gcc -O3 -march=native -o pi_native pi.c -lm
gcc -Ofast -o pi_aggressive pi.c -lm
gcc -Ofast -march=native -o pi_native_aggressive pi.c -lm


Run the 4 binaries and compare the performance:
./pi_std
./pi_native
./pi_aggressive
./pi_native_aggressive

Where they about the same?
Or very different?

Optional: Try a debug build:
gcc -g -o pi_dbg pi.c -lm

How is the speed of this one?
./pi_dbg

Check if and where vectorization happened
-----------------------------------------
gcc -O3 -o pi_std pi.c -lm -fopt-info-vec
gcc -O3 -march=native -o pi_native pi.c -lm -fopt-info-vec
gcc -Ofast -o pi_aggressive pi.c -lm -fopt-info-vec
gcc -Ofast -march=native -o pi_native_aggressive pi.c -lm -fopt-info-vec

Do you see any corellation between observed speed and the areas that were vectorized?

Check the generated code
------------------------
gcc -Ofast -march=native -o pi_native_aggressive pi.c -lm -fopt-info-vec -g -fverbose-asm -save-temps

Explore
pi.s

Look for comments mentioning
pi.c:23

