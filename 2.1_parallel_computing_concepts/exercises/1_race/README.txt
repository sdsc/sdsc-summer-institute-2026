Simple example of a race condition in a counter
===============================================

Compile
-------

module load gcc/10.2.0
g++ -fopenmp omp_race.cpp dummy_function.cpp -o omp_race

Run
---

#sequential, as verification
OMP_NUM_THREADS=1 ./omp_race 

#parallel, hit race condition
./omp_race 
