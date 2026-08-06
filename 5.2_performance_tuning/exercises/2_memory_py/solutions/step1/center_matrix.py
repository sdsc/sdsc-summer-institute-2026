import sys
import time
import numpy
from numba import njit, prange

# Note: This will be compiled by numba on the fly
#       It is conceptually equivalent to OpenMP
@njit(parallel=True)
def mat_init(m,i):
    n = m.shape[0]
    # prange is the equivalent of omp parallel for
    for col in prange(n):
      for row in range(n):
        m[col,row] = 0.1*col-0.15*row
    # just change one element to avoid over-optimization
    m[i%n,0]+=1

# compute m*m*a, update in-place and return the mean
@njit(parallel=True)
def square_update_and_mean(m,a):
    n = m.shape[0]
    gsum = numpy.float64(0.0)
    # prange is the equivalent of omp parallel for
    # no need to explicitly specify reduction
    # numba wil auto-detect
    for col in prange(n):
      rowsum = numpy.float64(0.0)
      for row in range(n):
        val = m[col,row]
        res = val*val*a     # compute square
        m[col,row] = res    # save result
        rowsum = rowsum + res           # use the result to also compute mean
      gsum += rowsum
    return gsum/numpy.float64(n*n)

# Note: Some steps have already been merged
# TODO: Further Optimize memory access
def centre_mean(m1):
  # was m1 = m*m*(-0.5)
  m1_mean = square_update_and_mean(m1,-0.5); # m1 is updated in place
  m2 = m1-m1.mean(axis=1, keepdims=True)-m1.mean(axis=0, keepdims=True)+m1_mean
  return m2.mean()

N = int(sys.argv[1])
iterations = int(sys.argv[2])

m0 = numpy.zeros([N,N])
# initialize once outside the timer, to avoid initial compilation cost
mat_init(m0,0)

t1 = time.time()

o = 0.0
# keep something to output, to avoid over-optimization
for i in range(iterations):
  # initialize in the loop, so centre_mean is free to update in-place, if so desired
  mat_init(m0,i)

  o += centre_mean(m0)

t2 = time.time()

print("Total time: %f, result %f\n"%(t2-t1,o))
