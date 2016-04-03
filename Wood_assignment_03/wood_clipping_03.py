# Wood, Jeff
# 100-103-5461
# 2016-04-08
# Assignment_03

import numpy as np

class outcode:    
    def __init__(self):
	self.left = 1
	self.right = 2
	self.bottom = 4
	self.top = 8
	self.near =16
	self.far = 32
	self.all = 0

    def CompOutCode(self, f_x, f_y, f_z, f_xmin, f_xmax, f_ymin, f_ymax, f_zmin, f_zmax)

	outcode code;
	
	code.top = 1;
	code.bottom = 2;
	code.left = 4;
	code.right = 8;
	code.near = 16;
	code.far = 32;
	code.all = 64;
	
	if (y > ymax) {
		code.top = 1;
	code.all += code.top;
	} else if (y < ymin) {
	code.bottom = 1;
	code.all += code.bottom;
	}
	if (x > xmax) {
	code.right = 1;
	code.all += code.right;
	} else if (x < xmin) {
	code.left = 1;
	code.all += code.left;
	}
	if (z > zmax) {
	code.far = 1;
	code.all += code.right;
	} else if (z < zmin) {
	code.near = 1;
	code.all += code.left;
	}
	return code;
}
void CohenSutherlandLineClipAndDraw (float x0, float y0, float z0, float x1, float y1, ffloat xmin, float xmax, float ymin, float ymax, float zmin, float zmax, int value)
/* Cohen-Sutherland clipping algorithm for line P0 = (x0, y0, z0) to P1 = (x1, y1, z1) a/* clip volume with diagonal from (xmin, ymin, zmin) to (xmax, ymax, zmax) */
{
	boolean accept, done;
	outcode outcode0, outcode1, outcodeOut, CompOutCode();
	float x, y, z;
	accept = FALSE;
	done = FALSE;
	outcode0 = CompOutCode(x0, y0, z0, xmin, xmax, ymin, ymax, zmin, zmax);
	outcode1 = CompOutCode(x1, y1, z1, xmin, xmax, ymin, ymax, zmin, zmax);
	do {
		if (outcode0.all == 0 && outcode1.all == 0) {
			accept = TRUE;
			done = TRUE;
		} else if (outcode0.all & outcode1.all != 0) {
			done = TRUE; /* Logical intersection is true, so trivial reject and exit */
		} else {
			if (outcode0.all != 0) {
				outcodeOut = outcode0;
			} else {
				outcodeOut = outcode1;
			}
			if (outcodeOut.top) {
				x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0);
				y = ymax;
				z = z0 + (z1 - z0) * (ymax - y0) / (y1 - y0);
			} else if (outcodeOut.bottom) {
				x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0);
				y = ymin;
				z = z0 + (z1 - z0) * (ymin - y0) / (y1 - y0);
			} else if (outcodeOut.right) {
				x = xmax;
				y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0);
				z = z0 + (z1 - z0) * (xmax - x0) / (x1 - x0);
			} else if (outcodeOut.left) {
				x = xmin;
				y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0);
				z = z0 + (z1 - z0) * (xmin - x0) / (x1 - x0);
			} else if (outcodeOut.near) {
				z = zmin;
			// stub .... your turn
			} else if (outcodeOut.far) {
				z = zmax;
				// stub .... your turn
			}
			if (outcodeOut.all == outcode0.all) {
				x0 = x;
				y0 = y;
				z0 = z;
				outcode0 = CompOutCode (x0, y0, xmin, xmax, ymin, ymax, zmin, zmax);
			} else {
				x1 = x;
				y1 = y;
				z1 = z;
				outcode1 = CompOutCode (x1, y1, xmin, xmax, ymin, ymax, zmin, zmax);
			}
		}
	} while(!done);
	if (accept)
		MidpointLineReal (x0,y0,z0,x1,y1,z1,value); /* Version for float coordinates */
}
