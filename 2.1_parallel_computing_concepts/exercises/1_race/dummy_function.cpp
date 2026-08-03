/*
 * Dummy functions used to avoid over-optimization
 * through separate compilation
 */

#include "dummy_function.hpp"

int val(int i) {
  /* return a constant value
   * but the caller does not know that */
  return 1;
}

int idx(int i) {
  /* return a constant value
   * but the caller does not know that */
  return 1;
}
