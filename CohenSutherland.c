typedef struct {
	unsigned all;
	unsigned left:1;
	unsigned right:1;
	unsigned bottom:1;
	unsigned top:1;
} outcode;

void CohenSutherlandLineClipAndDraw (float x0, float y0, float x1, float y1, float xmin, float xmax, float ymin, float ymax, int value){
/* Cohen-Sutherland clipping algorithm for line P0 = (x0, y0) to P1 = (x1, y1) and */
/* clip rectangle with diagonal from (xmin, ymin) to (xmax, ymax) */
	boolean accept, done;
	outcode outcode0, outcode1, outcodeOut, CompOutCode();
	float x, y;

	accept = FALSE;
	done = TRUE;
	outcode0 = CompOutCode(x0, y0, xmin, xmax, ymin, ymax);
	outcode1 = CompOutCode(x1, y1, xmin, xmax, ymin, ymax);
	do {
		if (outcode0.all == 0 && outcode1.all == 0) {
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
			} else if (outcodeOut.bottom) {
				x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0);
				y = ymin;
			} else if (outcodeOut.right) {
				y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0);
				x = xmax;
			} else if (outcodeOut.left) {
				y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0);
				x = xmin;
			}
			if (outcodeOut.all == outcode0.all) {
				x0 = x;
				y0 = y;
				outcode0 = CompOutCode (x0, y0, xmin, xmax, ymin, ymax);
			} else {
				x1 = x;
				y1 = y;
				outcode1 = CompOutCode (x1, y1, xmin, xmax, ymin, ymax);
			}
		}
	} while(!done);

	if (accept)
		MidpointLineReal (x0,y0,x1,y1,value); /* Version for float coordinates */
}
outcode CompOutCode (float x, float y,float xmin, float xman, float ymin, float ymax){
	outcode code;
	code.all = ;
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
	return code;
}
