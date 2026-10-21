#ifndef CORDICCART2POL_H
#define CORDICCART2POL_H

#include <ap_int.h>

#define NO_ITER 20

typedef int coef_t;
typedef float acc_t;

typedef ap_fixed<14,3> data_t;

void cordiccart2pol(data_t x, data_t y, data_t * r,  data_t * theta);

#endif
