The impact of separate compilation
==================================

This simple C program computes PI several times.
The code is split into two separate files, like it is common practice when one has a large code-base.

Build and test setup
--------------------

Start an interactive session with
srun --partition=shared --reservation=si26cpu --account=sdp173 --pty --nodes=1 --ntasks-per-node=1 --mem=8G -c 4 -t 00:30:00 /bin/bash
(Adapt partition/reservation/account if needed)

Then load the correct compiler
module load gcc/10.2.0

Build the two files with maximum optimization
---------------------------------------------

Separate compilation is common practice in large code-bases:
gcc -Ofast -march=native -o pi_library.o -c pi_library.c -lm -fopt-info-vec
gcc -Ofast -march=native -o pi pi.c  pi_library.o -lm -fopt-info-vec

Did you see the expected vectorization?

Try to run it:
./pi

Did it perform as expected?

Bundle the compilation phases
-----------------------------

You can build both files with a single command:
rm -f pi_library.o
gcc -Ofast -march=native -o pi2 pi.c pi_library.c -lm -fopt-info-vec

Did that improve vectorization?

Is the binary any faster?
./pi2

Include the source not the header
---------------------------------

While including the header is the standard practice,
nothing prevents you from including the source code itself.
(the .c file becomes de-facto a header file)

So, edit pi.c, and replace the pi_library include from .h to .c .

Now compile again (no need to explicity mention the library source file anymore):
rm -f pi_library.o
gcc -Ofast -march=native -o pi_one pi.c -lm -fopt-info-vec

Did that improve vectorization?

Is the binary any faster?
./pi_one

Optional split compilation of center_matrix
-------------------------------------------

Go back to exercise
2_memory
and move the implementation of the constexpr helper methods into another (library) file,
and separately compile that.
(You must remove constexpr property for separate compilarion to succeeed, since constexpr implies inline.)

How did performance change?

What happens if you move all the class methods' implementations into the library source file?

With only ex-constexpr methods in the library file,
can you keep separate compilation, but use vector types instead of scalar double?
How close can you get to the original speed that way?


Additional optional exercises
------------------
Pick any other exercise source file (from any session) that has functions and/or methods in the same file,
split the implementation of those functions/methods into another file,
and then check if/how the separate compilation affects the vectorization and performance of the executable.

