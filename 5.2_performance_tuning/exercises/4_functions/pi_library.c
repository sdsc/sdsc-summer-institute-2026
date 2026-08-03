/*
 * Simple PI helper
 */

#include "pi_library.h"

// Use Leibniz formula
double one_pi_step(int i) {
  return (4.0 / (2.0*i+1.0));
}
