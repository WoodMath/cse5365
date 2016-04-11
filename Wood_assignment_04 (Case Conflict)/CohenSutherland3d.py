# Wood, Jeff
# 100-103-5461
# 2016-04-08
# Assignment_03

#   From:
#       http://www.jesshamrick.com/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/
#       http://jfine-python-classes.readthedocs.org/en/latest/subclass-int.html
#       https://docs.python.org/2/tutorial/classes.html
#       https://docs.python.org/3.5/tutorial/classes.html
#       http://stackoverflow.com/questions/1607612/python-how-do-i-make-a-subclass-from-a-superclass
#       http://learnpythonthehardway.org/book/ex44.html

import numpy as np

class OutCode:
    def __init__(self):
        self.all = 0
        self.left = 1
        self.right = 2
        self.bottom = 4
        self.top = 8
        self.near = 16
        self.far = 32

def CompOutCode(f_x, f_y, f_z, f_xmin, f_xmax, f_ymin, f_ymax, f_zmin, f_zmax):
    code = OutCode()

    code.all = 0
    code.left = 1
    code.right = 2
    code.bottom = 4
    code.top = 8
    code.near = 16
    code.far = 32

    ## Check for being insidie X boundaries
    if (f_x < f_xmin):
        code.left = 1
        code.all += code.left
    elif (f_xmax < f_x):
        code.right = 2
        code.all += code.right
            
    ## Check for being insidie Y boundaries
    if (f_y < f_ymin):
        code.bottom = 4
        code.all += code.bottom
    elif (f_ymax < f_y):
        code.top = 8
        code.all += code.top

    ## Check for being insidie Z boundaries	
    if (f_z < f_zmin):
        code.near = 16
        code.all += code.near
    elif (f_zmax < f_z):
        code.far = 32
        code.all += code.far

    return code

def CohenSutherlandLineClipAndDraw(f_x0, f_y0, f_z0, f_x1, f_y1, f_z1, f_xmin, f_xmax, f_ymin, f_ymax, f_zmin, f_zmax, i_value):

    ## Cohen-Sutherland clipping algorithm for line
    ##      P0 = (x0, y0, z0) to P1 = (x1, y1, z1)
    ##  a clip volume with diagonal
    ##  from (xmin, ymin, zmin) to (xmax, ymax, zmax)
    b_accept = False
    b_done = False

    outcode1 = OutCode()
    outcode0 = OutCode()
    outcodeOut = OutCode()

    f_x = None
    f_y = None
    f_z = None

    outcode0 = CompOutCode(f_x0, f_y0, f_z0, f_xmin, f_xmax, f_ymin, f_ymax, f_zmin, f_zmax)
    outcode1 = CompOutCode(f_x1, f_y1, f_z1, f_xmin, f_xmax, f_ymin, f_ymax, f_zmin, f_zmax)
    while(not b_done):
        if (outcode0.all == 0 and outcode1.all == 0):
            b_accept = True
            b_done = True

        elif ((outcode0.all & outcode1.all) != 0):
            b_done = True; ## Logical intersection is true, so trivial reject and exit
        else:
            if (outcode0.all != 0):
                outcodeOut = outcode0
            else:
                outcodeOut = outcode1

            if (outcodeOut.left):
                f_x = f_xmin
                f_y = f_y0 + (f_y1 - f_y0) * (f_xmin - f_x0) / (f_x1 - f_x0)
                f_z = f_z0 + (f_z1 - f_z0) * (f_xmin - f_x0) / (f_x1 - f_x0)
            elif (outcodeOut.right):
                f_x = f_xmax
                f_y = f_y0 + (f_y1 - f_y0) * (f_xmax - f_x0) / (f_x1 - f_x0)
                f_z = f_z0 + (f_z1 - f_z0) * (f_xmax - f_x0) / (f_x1 - f_x0)
            elif (outcodeOut.bottom):
                f_x = f_x0 + (f_x1 - f_x0) * (f_ymin - f_y0) / (f_y1 - f_y0)
                f_y = f_ymin
                f_z = f_z0 + (f_z1 - f_z0) * (f_ymin - f_y0) / (f_y1 - f_y0)
            elif (outcodeOut.top):
                f_x = f_x0 + (f_x1 - f_x0) * (f_ymax - f_y0) / (f_y1 - f_y0)
                f_y = f_ymax
                f_z = f_z0 + (f_z1 - f_z0) * (f_ymax - f_y0) / (f_y1 - f_y0)
            elif (outcodeOut.near):
                f_x = f_x0 + (f_x1 - f_x0) * (f_zmin - f_z0) / (f_z1 - f_z0)
                f_y = f_y0 + (f_y1 - f_y0) * (f_zmin - f_z0) / (f_z1 - f_z0)
                f_z = f_zmin
            elif (outcodeOut.far):
                f_x = f_x0 + (f_x1 - f_x0) * (f_zmax - f_z0) / (f_z1 - f_z0)
                f_y = f_y0 + (f_y1 - f_y0) * (f_zmax - f_z0) / (f_z1 - f_z0)
                f_z = f_zmax


            if (outcodeOut.all == outcode0.all):
                f_x0 = f_x
                f_y0 = f_y
                f_z0 = f_z
                outcode0 = CompOutCode (f_x0, f_y0, f_xmin, f_xmax, f_ymin, f_ymax, f_zmin, f_zmax)
            else:
                f_x1 = f_x
                f_y1 = f_y
                f_z1 = f_z
                outcode1 = CompOutCode (f_x1, f_y1, f_xmin, f_xmax, f_ymin, f_ymax, f_zmin, f_zmax);

    return b_accept

