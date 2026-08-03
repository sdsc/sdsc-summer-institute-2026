Simple example of using atomics to avoid race condition in a counter
====================================================================

Compile
-------

module load gcc/10.2.0
g++ -fopenmp omp_atomic.cpp dummy_function.cpp -o omp_atomic

Run
---

#sequential, as verification
OMP_NUM_THREADS=1 ./omp_atomic

#parallel, still no race condition
./omp_atomic
