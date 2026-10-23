#include "cordiccart2pol.h"

data_t angles[NO_ITER] = {0.785398163397448,	0.463647609000806,	0.244978663126864,	0.124354994546761,	0.0624188099959574,	0.0312398334302683,	0.0156237286204768,	0.00781234106010111,	0.00390623013196697,	0.00195312251647882,	0.000976562189559320,	0.000488281211194898,	0.000244140620149362,	0.000122070311893670,	6.10351561742088e-05,	3.05175781155261e-05};

const data_t INV_GAIN = 0.60725293505; //Assuming 16 rotations
const data_t HALF_PI = 1.57079632679;

void cordiccart2pol(data_t x, data_t y, data_t * r,  data_t * theta)
{
	// Write your code here
	#pragma HLS INTERFACE mode=s_axilite port=return
    #pragma HLS INTERFACE mode=s_axilite port=x
    #pragma HLS INTERFACE mode=s_axilite port=y
    #pragma HLS INTERFACE mode=s_axilite port=r
    #pragma HLS INTERFACE mode=s_axilite port=theta

	data_t x_current, y_current, theta_current;

	//Initial 90 degree rotation so that the vector lies in Quadrant I/IV
	if( y >= 0 ) //rotating clockwise by 90 degrees
	{
		x_current = y;
		y_current = -x;
		theta_current = HALF_PI;
	}
	else
	{
		x_current = -y;
		y_current = x;
		theta_current = -HALF_PI;
	}
	for( int j = 0; j < NO_ITER; j++)
	{
		data_t x_shift = x_current >> j; 
		data_t y_shift = y_current >> j;

		if (y_current > 0)
		{
			x_current += y_shift;
			y_current -= x_shift;
			theta_current += angles[j];
		}
		else
		{
			x_current -= y_shift;
			y_current += x_shift;
			theta_current -= angles[j];
		}
	}

	*r = x_current * INV_GAIN;
	*theta = theta_current;


	
}
