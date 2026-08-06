Optimizing for memory locality
===============================

Centering of a matrix is important for many analysis activities, for example in bioinformatics.

The procedure for computing it is quite simple;
here is a Python example from scikit-bio:
    input = raw_input*raw_input*(-0.5)
    row_means = input.mean(axis=1, keepdims=True)
    col_means = input.mean(axis=0, keepdims=True)
    matrix_mean = input.mean()
    output = input - row_means - col_means + matrix_mean

In this exercise, you start with that in
center_matrix.py

Can you make it go any faster?

Build and run environment
-------------------------

Start an interactive session with
srun --partition=shared --reservation=si26cpu --account=sdp173 --pty --nodes=1 --ntasks-per-node=1 --mem=64G -c 4 -t 00:30:00 /bin/bash
(Adapt partition/reservation/account if needed)

Then load the correct compiler
module load gcc/10.2.0 py-pip/21.1.2

Create a virtual environment with
module load py-virtualenv/16.7.6
virtualenv venv

Now you can activate the virtual environment with
source venv/bin/activate

and install numba (not available as a module on Expanse)
pip install numba


Try the provided source code
----------------------------

Let's check if the code scales nicely with larger sizes.

Measure the time it takes to compute a 6400^2 matrix 10 times:
python center_matrix.py 6400 10

Now measure how long it takes to compute 100^2 matrix 40960 times (64*64*10):
python center_matrix.py 100 40960

Finally, measure how long it takes to compute 50^2 matrix 163840 times (128*128*10):
python center_matrix.py 50 163840

If the code were perfectly scalable, it would take exactly the same amount of time.


Beware the cache line conflicts
-------------------------------

Try benchmarking a matrix that is a multiple of 1024, e.g.
python center_matrix.py 6144 10

compare to 
python center_matrix.py 6143 10
and
python center_matrix.py 6145 10


Optimize for memory locality
----------------------------

Your job is to speed up the application (for large matrices), by exploiting memory locality.
You will need to use numba for that.

Here are some hints:
a) Try to compute in-place, instead of creating new buffers
b) Try to go over each buffer only once
c) Avoid accessing buffers, use local variables as much as you can
d) Consider tiling if you need to iterate over columns

Every time you make a change that you think should make the code faster, re-measure.


