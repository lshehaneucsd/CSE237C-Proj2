#ifndef CORDICCART2POL_H
#define CORDICCART2POL_H

#include <ap_int.h>

#define NO_ITER 16

typedef int   coef_t; // what is this for?
typedef ap_fixed<16,3> data_t; // ap_fixed<16,1> 1 int bit?
typedef float acc_t; // what is this for?

void cordiccart2pol(data_t x, data_t y, data_t * r,  data_t * theta);

#endif
