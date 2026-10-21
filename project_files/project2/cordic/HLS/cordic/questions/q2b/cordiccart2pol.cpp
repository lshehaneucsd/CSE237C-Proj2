#include "cordiccart2pol.h"

data_t Kvalues[20] = {1, 0.500000000000000, 0.250000000000000, 0.125000000000000, 0.0625000000000000, 0.0312500000000000, 0.0156250000000000, 0.00781250000000000, 0.00390625000000000, 0.00195312500000000, 0.000976562500000000, 0.000488281250000000, 0.000244140625000000, 0.000122070312500000, 6.10351562500000e-05, 3.05175781250000e-05, 1.52587890625000e-05, 7.62939453125000e-06, 3.81469726562500e-06, 1.90734863281250e-06};

data_t angles[20] = {0.785398163397448, 0.463647609000806, 0.244978663126864, 0.124354994546761, 0.0624188099959574, 0.0312398334302683, 0.0156237286204768, 0.00781234106010111, 0.00390623013196697, 0.00195312251647882, 0.000976562189559319, 0.000488281211194898, 0.000244140620149362, 0.000122070311893670, 6.10351561742088e-05, 3.05175781155261e-05, 1.52587890613158e-05, 7.62939453110197e-06, 3.81469726560650e-06, 1.90734863281019e-06};

const data_t HALF_PI = 1.57079632;
const data_t INV_CORDIC_GAIN = 0.60725293505;

void cordiccart2pol(data_t x, data_t y, data_t * r,  data_t * theta)
{
  // Write your code here

  // look at https://kastner.ucsd.edu/hlsbook/ pg 76
  // this

  // look at https://en.wikipedia.org/wiki/CORDIC
  // this cordic converts a, n to <x,y>

  data_t x_current;
  data_t y_current;
  data_t theta_current;

  // goal is to rotate the vector <x,y> to be on the x axis
  // we find the length r as r = x
  // we find the angle theta as <x,y> rotated by theta will be <r,0>

  // initial 90 degree rotation to fix the quadrant
  // but if it is in Quadrant 1 or 4, it swaps, to remove a conditional
	if (y >=0){ // cw rotation
    x_current = y;
		y_current = - x;
    theta_current = HALF_PI;
	}
	else // ccw rotation
  {
		x_current = - y;
    y_current = x;
    theta_current = -HALF_PI;
  }

	for (int j=0; j<NO_ITER; j++){
    // set the shift first
    // data_t x_temp = x_current >> j;
    // data_t y_temp = y_current >> j;
    data_t x_temp = x_current * Kvalues[j]; // SHOULD I SWITCH to SHIFTS?
    data_t y_temp = y_current * Kvalues[j];

		if (y_current > 0){ // negative ccw rotation
      x_current += y_temp;
      y_current -= x_temp;
      theta_current += angles[j];
		}
		else // positive cw rotation
    {
      x_current -= y_temp;
      y_current += x_temp;
      theta_current -= angles[j];
    }
  }

  *r = x_current * INV_CORDIC_GAIN;
  *theta = theta_current;
}
