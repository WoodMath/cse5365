# Wood, Jeff
# 100-103-5461
# 2016-04-19
# Assignment_04

#   From:
#       http://www.jesshamrick.com/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/
#       http://jfine-python-classes.readthedocs.org/en/latest/subclass-int.html
#       https://docs.python.org/2/tutorial/classes.html
#       https://docs.python.org/3.5/tutorial/classes.html
#       http://stackoverflow.com/questions/1607612/python-how-do-i-make-a-subclass-from-a-superclass
#       http://learnpythonthehardway.org/book/ex44.html

import numpy as np

class Point:
    def __init__(self, f_x=None, f_y=None, f_z=None):
        self.x = f_x
        self.y = f_y
        self.z = f_z
        self.v3 = None
        self.updateV3()
    def updateV3(self):
        self.v3 = [self.x, self.y, self.z]
    def setPoint(self, f_x, f_y, f_z):
        v3_point = [f_x, f_y, f_z]
        self.x = v3_point[0]
        self.y = v3_point[1]
        self.z = v3_point[2]
        self.updateV3()
    def getPointV3(self):
        return [self.x, self.y, self.z]
    def getPointV4(self):
        return [self.x, self.y, self.z, 1]
    def get(self):
        return self

class Plane:
    def __init__(self):
        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.vector = None
    def set(self, v_set):
        self.vector

class PlaneOperation(Plane):
    def __init__(self):
        Plane.__init__(self):
        self.commonPoint = [0,0,0.5,1]

    def test(none, v_plane, v_pass):
        # Two points will be on same side of hyperplane ...
        
        # ... if the dot of each point with the plane ...

        if(len(v_point)==3):
            v_point = [v_pass[0],v_pass[1],v_pass[2],1]
        else
            v_point = copy.copy(v_pass)
        
        v_common_dot = np.dot(v_plane, self.commonePoint)
        v_point_dot = np.dot(v_plane, v_point)

        # ... results in numbers with the same sign.
        b_Return = True if v_common_dot * v_point_dot > 0 else False
        return b_Return


class ClippingVolume:
    def __init__(self):
        ## Using normal of planes
        self.xMin = [1,0,0,1]
        self.xMax = [-1,0,0,1]
        self.yMin = [0,1,0,1]
        self.yMax = [0,-1,0,1]
        self.zMin = [0,0,1,0]
        self.zMax = [0,0,-1,1]
        self.commonPoint = [0,0,0.5,1]

    def test(none, v_plane, v_pass):
        # Two points will be on same side of hyperplane ...
        
        # ... if the dot of each point with the plane ...

        if(len(v_point)==3):
            v_point = [v_pass[0],v_pass[1],v_pass[2],1]
        else
            v_point = copy.copy(v_pass)
        
        v_common_dot = np.dot(v_plane, self.commonePoint)
        v_point_dot = np.dot(v_plane, v_point)

        # ... results in numbers with the same sign.
        b_Return = True if v_common_dot * v_point_dot > 0 else False
        return b_Return
    
    def get(self):
        return {'xMin':self.xMin, 'xMax':self.xMax, 'yMin':self.yMin, 'yMax':self.yMax, 'zMin':self.zMin, 'zMax':self.zMax}


class OutCode:
    def __init__(self):
        self.all = 0
        self.left = 1
        self.right = 2
        self.bottom = 4
        self.top = 8
        self.near = 16
        self.far = 32
    def hasLeft(self):
        return (self.all & self.left)
    def hasRight(self):
        return (self.all & self.right)
    def hasBottom(self):
        return (self.all & self.bottom)
    def hasTop(self):
        return (self.all & self.top)
    def hasNear(self):
        return (self.all & self.near)
    def hasFar(self):
        return (self.all & self.far)
    def get(self):
        return {'all':self.all, 'left':self.left, 'right':self.right, 'bottom':self.bottom, 'top':self.top, 'near':self.near, 'far':self.far}

class Clipping:
    def __init__(self):
        self.point0old = Point()
        self.point1old = Point()
        self.cv = ClippingVolume()
        self.done = False
        self.accept = False
        self.point0new = Point()
        self.point1new = Point()
    def setPoint0(self, f_x0, f_y0, f_z0):
        self.point0old.setPoint(f_x0, f_y0, f_z0)
        self.point0new = copy.copy(self.point0old)
    def setPoint1(self, f_x1, f_y1, f_z1):
        self.point1old.setPoint(f_x1, f_y1, f_z1)
        self.point1new = copy.copy(self.point1old)
        
    def getOutCode(self, point):
        code = OutCode()
        cv = self.cv

        f_x = point.x
        f_y = point.y
        f_z = point.z

        v_xmin = self.cv.xMin
        v_xmax = self.cv.xMax
        v_ymin = self.cv.yMin
        v_ymax = self.cv.yMax
        v_zmin = self.cv.zMin
        v_zmax = self.cv.zMax

        v1_test = [f_x, f_y, f_z, 1]

        ## Check for being insidie X boundaries
        if (not(self.cv.test(v_xmin,v1_test))):
            code.left = 1
            code.all += code.left
        elif (not(self.cv.test(v_xmax,v1_test))):
            code.right = 2
            code.all += code.right
                
        ## Check for being insidie Y boundaries
        if (not(self.cv.test(v_ymin,v1_test))):
            code.bottom = 4
            code.all += code.bottom
        elif (not(self.cv.test(v_ymax,v1_test))):
            code.top = 8
            code.all += code.top

        ## Check for being insidie Z boundaries	
        if (not(self.cv.test(v_zmin,v1_test))):
            code.near = 16
            code.all += code.near
        elif (not(self.cv.test(v_zmax,v1_test))):
            code.far = 32
            code.all += code.far

        return code
    
    def setPoint0(self, f_x0, f_y0, f_z0):
        self.point0old.setPoint(f_x0, f_y0, f_z0)
        self.point0new.setPoint(f_x0, f_y0, f_z0)
        #self.point0new = copy.copy(self.point0old)
    def setPoint1(self, f_x1, f_y1, f_z1):
        self.point1old.setPoint(f_x1, f_y1, f_z1)
        self.point1new.setPoint(f_x1, f_y1, f_z1)
        #self.point1new = copy.copy(self.point1old)
        
    def draw():
        return self.accept
    def getPoint0(self):
        return self.point0new
    def getPoint1(self):
        return self.point1new

    def calcLine(self):

        cv = self.cv
        
        ## Cohen-Sutherland clipping algorithm for line
        ##      P0 = (x0, y0, z0) to P1 = (x1, y1, z1)
        ##  a clip volume with diagonal
        ##  from (xmin, ymin, zmin) to (xmax, ymax, zmax)
        self.accept = False
        self.done = False

        outCode0 = OutCode()
        outCode1 = OutCode()
        outCodeOut = OutCode()

        f_x = None
        f_y = None
        f_z = None

        f_xmin = self.cv.xMin
        f_xmax = self.cv.xMax
        f_ymin = self.cv.yMin
        f_ymax = self.cv.yMax
        f_zmin = self.cv.zMin
        f_zmax = self.cv.zMax

        f_x0 = self.point0old.x
        f_y0 = self.point0old.y
        f_z0 = self.point0old.z

        f_x1 = self.point1old.x
        f_y1 = self.point1old.y
        f_z1 = self.point1old.z


        ## Solve 0 = v_plane*(v_one + v_zero*t) for t where
        ##      v_plane = [A,B,C,D]                                         ## Where A*x+B*y+C*z+D*1=0
        ##      v_one = [f_x0, f_y0, f_z0, 1]^T                             ## Has trailing 1
        ##      v_zero = [f_x1-f_x0, f_x1-f_x0, f_x1-f_x0, 0]^T             ## Has trailing 0
        
        v0_point0 = [f_x0, f_y0, f_z0, 0] 
        v0_point1 = [f_x0, f_y0, f_z0, 1] 



        v1_point0 = [f_x1, f_y1, f_z1, 0] 
        v1_point1 = [f_x1, f_y1, f_z1, 1] 

        outCode0 = self.getOutCode(self.point0old)
        outCode1 = self.getOutCode(self.point1old)
        while(not self.done):
            if (outCode0.all == 0 and outCode1.all == 0):
                self.accept = True
                self.done = True ## Logical intersection is true, so trivial reject and exit

            elif ((outCode0.all & outCode1.all) != 0):
#                print(' We Done !')
                self.done = True; ## Logical intersection is true, so trivial reject and exit
            else:
#                print(' We NOT Done !')
                if (outCode0.all != 0):
                    outCodeOut = outCode0
#                else:
                if (outCode1.all != 0):
                    outCodeOut = outCode1

#                print(' outCodeOut = ' + str(outCodeOut.get()))

                if (outCodeOut.hasLeft()):                    
                    f_x = f_xmin
                    f_y = f_y0 + (f_y1 - f_y0) * (f_xmin - f_x0) / (f_x1 - f_x0)
                    f_z = f_z0 + (f_z1 - f_z0) * (f_xmin - f_x0) / (f_x1 - f_x0)
                elif (outCodeOut.hasRight()):
                    f_x = f_xmax
                    f_y = f_y0 + (f_y1 - f_y0) * (f_xmax - f_x0) / (f_x1 - f_x0)
                    f_z = f_z0 + (f_z1 - f_z0) * (f_xmax - f_x0) / (f_x1 - f_x0)
                elif (outCodeOut.hasBottom()):
                    f_x = f_x0 + (f_x1 - f_x0) * (f_ymin - f_y0) / (f_y1 - f_y0)
                    f_y = f_ymin
                    f_z = f_z0 + (f_z1 - f_z0) * (f_ymin - f_y0) / (f_y1 - f_y0)
                elif (outCodeOut.hasTop()):
                    f_x = f_x0 + (f_x1 - f_x0) * (f_ymax - f_y0) / (f_y1 - f_y0)
                    f_y = f_ymax
                    f_z = f_z0 + (f_z1 - f_z0) * (f_ymax - f_y0) / (f_y1 - f_y0)
                elif (outCodeOut.hasNear()):
                    f_x = f_x0 + (f_x1 - f_x0) * (f_zmin - f_z0) / (f_z1 - f_z0)
                    f_y = f_y0 + (f_y1 - f_y0) * (f_zmin - f_z0) / (f_z1 - f_z0)
                    f_z = f_zmin
                elif (outCodeOut.hasFar()):
                    f_x = f_x0 + (f_x1 - f_x0) * (f_zmax - f_z0) / (f_z1 - f_z0)
                    f_y = f_y0 + (f_y1 - f_y0) * (f_zmax - f_z0) / (f_z1 - f_z0)
                    f_z = f_zmax


                if (outCodeOut.all == outCode0.all):
                    f_x0 = f_x
                    f_y0 = f_y
                    f_z0 = f_z
                    self.point0new.setPoint(f_x0, f_y0, f_z0)
                    outCode0 = self.getOutCode(self.point0new)
#                else:
                if (outCodeOut.all == outCode1.all):
                    f_x1 = f_x
                    f_y1 = f_y
                    f_z1 = f_z
                    self.point1new.setPoint(f_x1, f_y1, f_z1)
                    outCode1 = self.getOutCode(self.point1new)

        
        return self.accept

def clipping_test():
    c=Clipping()
    p0=Point(0.25,0.25,0.25)
    p1=Point(0.75,0.75,0.75)

    print(' **** ')

    print(' p0 = ' + str(p0.getPointV3()))
    print(' c.getOutCode(p0) = ' + str(c.getOutCode(p0).all))
    print(' p1 = ' + str(p1.getPointV3()))
    print(' c.getOutCode(p1) = ' + str(c.getOutCode(p1).all))

    c.setPoint0(0.5,-1.5,0.5)
    c.setPoint1(0.5,-2.5,0.5)

    c.calcLine()

    print(' **** ')

    print(' c.point0old = ' + str(c.point0old.getPointV3()))
    print(' c.getOutCode(c.point0old) = ' + str(c.getOutCode(c.point0old).all))
    print(' c.point1old = ' + str(c.point1old.getPointV3()))
    print(' c.getOutCode(c.point1old) = ' + str(c.getOutCode(c.point1old).all))

    print(' **** ')

    print(' c.point0new = ' + str(c.point0new.getPointV3()))
    print(' c.getOutCode(c.point0new) = ' + str(c.getOutCode(c.point0new).all))
    print(' c.point1new = ' + str(c.point1new.getPointV3()))
    print(' c.getOutCode(c.point1new) = ' + str(c.getOutCode(c.point1new).all))

    c.setPoint0(-1.5,-1.5,-1.5)
    c.setPoint1(1.5,1.5,1.5)

    c.calcLine()

    print(' **** ')

    print(' c.point0old = ' + str(c.point0old.getPointV3()))
    print(' c.getOutCode(c.point0old) = ' + str(c.getOutCode(c.point0old).all))
    print(' c.point1old = ' + str(c.point1old.getPointV3()))
    print(' c.getOutCode(c.point1old) = ' + str(c.getOutCode(c.point1old).all))

    print(' **** ')

    print(' c.point0new = ' + str(c.point0new.getPointV3()))
    print(' c.getOutCode(c.point0new) = ' + str(c.getOutCode(c.point0new).all))
    print(' c.point1new = ' + str(c.point1new.getPointV3()))
    print(' c.getOutCode(c.point1new) = ' + str(c.getOutCode(c.point1new).all))


