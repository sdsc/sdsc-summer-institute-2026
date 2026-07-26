/*
 * Example of a race condition.
 */

#include <cstdlib>
#include <cstdio>

#include "dummy_function.hpp"


void run_parallel(int N) {
  int bufsize = 2+N/10000;

  int *cnts = new int[bufsize];
  for (int i=0; i<bufsize; i++) cnts[i] = 0;

  /*
   * Note: The += in this loop abviously has a race condition
   *       if run in parallel.
   *       Since bufsize<N, at least two iterations
   *       will write in the same location.
   *
   * No reasonable compiler would auto-vectorize this code.
   * But pragma omp parallel forces parallelization.
   */
#pragma omp parallel for
  for (int i=0; i<N; i++) cnts[idx(i)] += val(i);

  // The compiler does not know it, but we were updating the same index with +1
  printf("Result: %i Expected %i\n",cnts[idx(0)],N);
  delete[] cnts;
}

int main(int argc, char *argv[]) {
  int N = 50000;

  if (argc>1) N = atoi(argv[1]);

  run_parallel(N);

  return 0;
}
