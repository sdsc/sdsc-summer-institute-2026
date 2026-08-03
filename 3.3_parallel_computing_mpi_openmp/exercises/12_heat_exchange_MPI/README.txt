2D Heat Diffusion
=================

High level problem overview
---------------------------

Imagine a massive square metal plate.
The edges of the plate are held at a constant freezing temperature, while the interior is initialized with a heat pattern.
Over time, the heat diffuses across the plate.
To calculate the temperature of any given point at the next time step, you take the average of its current temperature and the temperatures of its four immediate neighbors (up, down, left, and right).
We are however not interested in temperatures at all the point, just the global average temperature.

The serial version
------------------

You can find the serial version for solving the problem in
heat_serial.c

Compile it with
gcc -o heat_serial -O3 heat_serial.c  -lm

And try it out
./heat_serial 

(Optional)
Make it OpenMP parallel.
It is very simple.

Make it MPI parallel
--------------------

The problem with solving this problem with partitioned memory,
is that you do not have access to the neighbours at the borders.

A common solution are so-called "ghost cells".
You essentally have overlapping elements that are present in multiple processes.
You then must keep them in sync after each iteration.

In this exercise, let's split the 2D matrix among M MPI processes
by splitting by rows, with every process owning N/M rows.
 
Each process also needs 2 ghost rows;
we will need them as input, as those rows contain the values from the neighbour process, so we must fetch from them before we start our own compute.
(Note that the top and bottom process do not need to worry about ghosts, as those are guaranteed to be always at freezing point)

You will also have to collect the total local sums into a single process, for printout.

Solving the problem with MPI is left as an exercise, but you can start with the comment-annotated
heat_mpi.c
if you want.
I actually recommend you try to refactor heat_serial directly.

Once you have the code ready, you execute it the same way as the other MPI exercise:
salloc --partition=shared --reservation=si26cpu --account=sdp173 --nodes=1 --mem=32G -n 8 -c 4 -t 00:30:00
(Adapt partition/reservation/account if needed)

module load gcc/10.2.0 openmpi/4.1.3
mpicc -o heat_mpi -O3 heat_mpi.c  -lm
srun -n 8 ./heat_mpi
 
The result should be identical to the serial version
(apart from possibly minor FP rounding errors)

Use multiple nodes
------------------

As with 11_axpy, try using 2 nodes
(Reminder, cannot use the shared partition)
salloc --partition=preempt --reservation=si26cpu --account=sdp173 --nodes=2 --mem=32G -n 8 -c 4 -t 00:30:00

You may try using a different number of MPI processes, too.
Just make sure you use the same number in salloc and srun.

e.g.
salloc --partition=preempt --reservation=si26cpu --account=sdp173 --nodes=2 --mem=32G -n 16 -c 4 -t 00:30:00
module load gcc/10.2.0 openmpi/4.1.3
srun -n 16 ./heat_mpi

