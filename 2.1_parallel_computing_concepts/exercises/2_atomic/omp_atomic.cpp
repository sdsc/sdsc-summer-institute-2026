/*
 * Example of a race condition.
 */

#include <cstdlib>
#include <cstdio>
#include <atomic>

#include "dummy_function.hpp"


void run_parallel(int N) {
  int bufsize = 2+N/10000;

  std::atomic_int *cnts = new std::atomic_int[bufsize];

#pragma omp parallel for
  for (int i=0; i<N; i++) cnts[idx(i)] += val(i);

  // The compiler does not know it, but we were updating the same index with +1
  printf("Result: %i Expected %i\n",cnts[idx(0)].load(),N);
  delete[] cnts;
}

int main(int argc, char *argv[]) {
  int N = 50000;

  if (argc>1) N = atoi(argv[1]);

  run_parallel(N);

  return 0;
}
