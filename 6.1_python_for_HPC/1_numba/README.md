# Numba notebooks

Numba turns supported Python and NumPy code into machine code. The core lesson
starts with one slow numerical loop. Students add `@jit`, check that the answer
is still correct, call the function once so Numba can compile it, and then time
later calls.

## Core

1. [`0_basics.ipynb`](0_basics.ipynb): add `@jit`, call the function once, check
   the answer, and time later calls.

## Optional deep dives

2. [`1_numpy.ipynb`](1_numpy.ipynb): how Numba handles different NumPy array
   types and custom array functions.
3. [`2_threads.ipynb`](2_threads.ipynb): use several threads inside one Numba
   function.
4. [`3_numba_groupby_pixels.ipynb`](3_numba_groupby_pixels.ipynb): optimize an
   authentic astronomy group-by calculation.

## Decision rule

Try Numba when timing shows that a numerical Python loop is slow and the same
work is hard to write as one clear NumPy expression. Prefer NumPy when it
already expresses the work clearly. Always check the result, call the compiled
function once, and then time later calls.

Optional notebooks are take-home material. Learners do not need to complete
them during the session.
