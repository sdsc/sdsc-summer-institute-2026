# Numba notebooks

Numba compiles a useful subset of Python and NumPy to machine code. The core
lesson starts with one hot loop and separates correctness, compilation, and
steady-state timing.

Since Numba 0.59, bare `@jit` defaults to nopython mode. `@njit` remains the
explicit alias for `@jit(nopython=True)`. The notebooks use `@njit` so the
intended compilation mode is visible at the point of use.

See Numba's current
[`@jit` documentation](https://numba.readthedocs.io/en/stable/user/jit.html)
for the compilation modes and decorator options.

## Core

1. [`0_basics.ipynb`](0_basics.ipynb): add `@njit`, warm up the function, verify
   the answer, and benchmark.

## Optional deep dives

2. [`1_numpy.ipynb`](1_numpy.ipynb): specialization by dtype and custom ufuncs.
3. [`2_threads.ipynb`](2_threads.ipynb): automatic parallelization and
   `prange`.
4. [`3_numba_groupby_pixels.ipynb`](3_numba_groupby_pixels.ipynb): optimize an
   authentic astronomy group-by calculation.

## Decision rule

Try Numba when profiling identifies a numerical Python loop that is difficult
to express as one efficient NumPy operation. Prefer clear NumPy when it already
expresses the operation well. Always verify the result and exclude the first
compilation from the benchmark.

Optional notebooks are take-home material. Learners do not need to complete
them during the session.
