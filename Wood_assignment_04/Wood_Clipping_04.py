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

iClippingRoundPlaces = 15

import numpy as np
import copy

class Point:
    def __init__(self, f_x=None, f_y=None, f_z=None, f_w=None):
        self.x = f_x
        self.y = f_y
        self.z = f_z
        self.w = f_w
        self.v3 = None
        self.v4 = None
        self.type = None
        self.updateV3()
        self.updateV4()
    def updateV3(self):
        self.v3 = [self.x, self.y, self.z]
    def updateV4(self):
        self.v4 = [self.x, self.y, self.z, self.w]
    def setPoint(self, f_x, f_y, f_z, f_w=None):
        if(f_w==None):
            f_w = 1
        v3_point = [f_x, f_y, f_z]
        v4_point = [f_x, f_y, f_z, f_w]
        self.x = f_x
        self.y = f_y
        self.z = f_z
        self.w = f_w
        self.updateV3()
        self.updateV4()
    def getPointV3(self):
        return [self.x, self.y, self.z]
    def getPointV4(self):
        if(self.type == 'parallel'):
            return [self.x, self.y, self.z, 1]
        if(self.type == 'perspective'):
            return [self.x, self.y, self.z, self.z]        
    def getHomoPointV4(self):
        v_temp = self.getPointV4()
        v_return = [v_temp[0]/v_temp[3], v_temp[1]/v_temp[3], v_temp[2]/v_temp[3], 1]
        return v_return
    def get(self):
        return {'x':self.x,'y':self.y,'z':self.z,'v3':self.v3}
    def setParallel(self):
        self.type = 'parallel'
    def setPerspective(self):
        self.type = 'perspective'
    def setType(self,s_type):
        self.type = s_type
        if(self.type == 'parallel'):
            self.setParallel()
        if(self.type == 'perspective'):
            self.setPerspective()

class ClippingVolume:
    def __init__(self):
        self.xMin = -1
        self.xMax = 1
        self.yMin = -1
        self.yMax = 1
        self.zMin = 0
        self.zMax = 1
        self.perspectiveNear = None
    def setParallel(self):
        self.type = 'parallel'
        print(' self.type = ' + str(self.type))

    def setPerspective(self):
        self.type = 'perspective'
        print(' self.type = ' + str(self.type))

    def setType(self,s_type):
        self.type = s_type
        if(s_type=='parallel'):
            self.setParallel()
        if(s_type=='perspective'):
            self.setPerspective()
    def setPerspectiveNear(self, perspectiveNear=None):
        print(' perspectiveNear = ' + str(perspectiveNear))
        if(self.type=='parallel'):
            return
        self.perspectiveNear = perspectiveNear
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
    def __init__(self,camera):
        self.point0old = Point()
        self.point1old = Point()
        self.cv = ClippingVolume()
        self.camera = camera
        self.done = False
        self.accept = False
        self.point0new = Point()
        self.point1new = Point()
        self.perspectiveNear = None
    def setPerspectiveNear(self,v_Dim_N, v_PRP):
        if(self.type == 'parallel'):
            return
        vDimN = np.array(v_Dim_N)
        vPRP = np.array(v_PRP)
        ## Use vVRP' = SH*T(-vPRP)*[0 0 0 1]^T
        fFar = vDimN[1] - vPRP[2] if abs(vDimN[1] - vPRP[2]) > abs(vDimN[0] - vPRP[2]) else vDimN[0] - vPRP[2]
        fNear = vDimN[0] - vPRP[2] if abs(vDimN[1] - vPRP[2]) > abs(vDimN[0] - vPRP[2]) else vDimN[1] - vPRP[2]
#        fFar = vDimN[1] + vVRP[2] if abs(vDimN[1] + vVRP[2]) > abs(vDimN[0] + vVRP[2]) else vDimN[0] + vVRP[2] 
#        fNear = vDimN[0] + vVRP[2] if abs(vDimN[1] + vVRP[2]) > abs(vDimN[0] + vVRP[2]) else vDimN[1] + vVRP[2]

        self.cv.setPerspectiveNear(fNear/fFar)
        self.perspectiveNear = fNear/fFar
        
    def setParallel(self):
        self.type = 'parallel'
        self.cv.setParallel()
        self.point0old.setParallel()
        self.point1old.setParallel()
        self.point0new.setParallel()
        self.point1new.setParallel()
        
    def setPerspective(self):
        self.type = 'perspective'
        self.cv.setPerspective()
        self.point0old.setPerspective()
        self.point1old.setPerspective()
        self.point0new.setPerspective()
        self.point1new.setPerspective()
        
    def setType(self,s_type):
        self.type = s_type
        self.cv.setType(s_type)
        if(self.type == 'parallel'):
            self.point0old.setParallel()
            self.point1old.setParallel()
            self.point0new.setParallel()
            self.point1new.setParallel()
        if(self.type == 'perspective'):
            self.point0old.setPerspective()
            self.point1old.setPerspective()
            self.point0new.setPerspective()
            self.point1new.setPerspective()
        
    def setPoint0(self, f_x0, f_y0, f_z0, f_w0=None):
        if(f_w0 == None):
            self.point0old.setPoint(f_x0, f_y0, f_z0, 1)
            self.point0new.setPoint(f_x0, f_y0, f_z0, 1)
        else:
            self.point0old.setPoint(f_x0, f_y0, f_z0, f_w0)
            self.point0new.setPoint(f_x0, f_y0, f_z0, f_w0)
        self.point0new = copy.copy(self.point0old)
        
    def setPoint1(self, f_x1, f_y1, f_z1, f_w1=None):
        if(f_w1 == None):
            self.point1old.setPoint(f_x1, f_y1, f_z1, 1)
            self.point1new.setPoint(f_x1, f_y1, f_z1, 1)
        else:
            self.point1old.setPoint(f_x1, f_y1, f_z1, f_w1)
            self.point1new.setPoint(f_x1, f_y1, f_z1, f_w1)
        self.point1new = copy.copy(self.point1old)

    def getPoint0(self):
        return self.point0new
    def getPoint1(self):
        return self.point1new

    def draw():
        return self.accept
    
    def getParallelOutCode(self, point):
        code = OutCode()

        f_x = point.x
        f_y = point.y
        f_z = point.z

        f_xmin = self.cv.xMin
        f_xmax = self.cv.xMax
        f_ymin = self.cv.yMin
        f_ymax = self.cv.yMax
        f_zmin = self.cv.zMin
        f_zmax = self.cv.zMax

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

    def calcParallelLine(self):
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

        f_x0 = round(self.point0old.x, iClippingRoundPlaces)
        f_y0 = round(self.point0old.y, iClippingRoundPlaces)
        f_z0 = round(self.point0old.z, iClippingRoundPlaces)

        f_x1 = round(self.point1old.x, iClippingRoundPlaces)
        f_y1 = round(self.point1old.y, iClippingRoundPlaces)
        f_z1 = round(self.point1old.z, iClippingRoundPlaces)

        outCode0 = self.getParallelOutCode(self.point0old)
        outCode1 = self.getParallelOutCode(self.point1old)
        while(not self.done):
            if (outCode0.all == 0 and outCode1.all == 0):
                self.accept = True
                self.done = True ## Logical intersection is true, so trivial reject and exit

            elif ((outCode0.all & outCode1.all) != 0):
                self.done = True; ## Logical intersection is true, so trivial reject and exit
            else:
                if (outCode0.all != 0):
                    outCodeOut = outCode0
                if (outCode1.all != 0):
                    outCodeOut = outCode1

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
                    outCode0 = self.getParallelOutCode(self.point0new)
                if (outCodeOut.all == outCode1.all):
                    f_x1 = f_x
                    f_y1 = f_y
                    f_z1 = f_z
                    self.point1new.setPoint(f_x1, f_y1, f_z1)
                    outCode1 = self.getParallelOutCode(self.point1new)
        
        return self.accept

    def getPerspectiveOutCode(self, point):
        code = OutCode()

        f_x = round(point.x, iClippingRoundPlaces)
        f_y = round(point.y, iClippingRoundPlaces)
        f_z = round(point.z, iClippingRoundPlaces)

        f_xmin = round(-point.z, iClippingRoundPlaces)
        f_xmax = round(point.z, iClippingRoundPlaces)
        f_ymin = round(-point.z, iClippingRoundPlaces)
        f_ymax = round(point.z, iClippingRoundPlaces)
        f_zmin = round(self.perspectiveNear, iClippingRoundPlaces)
        f_zmax = round(1, iClippingRoundPlaces)

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

    def calcPerspectiveLine(self):
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

        f_x0 = self.point0old.x
        f_y0 = self.point0old.y
        f_z0 = self.point0old.z

        f_x1 = self.point1old.x
        f_y1 = self.point1old.y
        f_z1 = self.point1old.z

        outCode0 = self.getPerspectiveOutCode(self.point0old)
        outCode1 = self.getPerspectiveOutCode(self.point1old)
        while(not self.done):
            if (outCode0.all == 0 and outCode1.all == 0):
                self.accept = True
                self.done = True ## Logical intersection is true, so trivial reject and exit

            elif ((outCode0.all & outCode1.all) != 0):
                self.done = True; ## Logical intersection is true, so trivial reject and exit
            else:
                if (outCode0.all != 0):
                    outCodeOut = outCode0
                if (outCode1.all != 0):
                    outCodeOut = outCode1

                if (outCodeOut.hasLeft()):
                    f_x = f_x0 - (f_x1 - f_x0) * (f_z0 + f_x0) / ((f_x1 - f_x0)+(f_z1 - f_z0))
                    f_y = f_y0 - (f_y1 - f_y0) * (f_z0 + f_x0) / ((f_x1 - f_x0)+(f_z1 - f_z0))
                    f_z = f_z0 - (f_z1 - f_z0) * (f_z0 + f_x0) / ((f_x1 - f_x0)+(f_z1 - f_z0))
                elif (outCodeOut.hasRight()):
                    f_x = f_x0 + (f_x1 - f_x0) * (f_z0 - f_x0) / ((f_x1 - f_x0)-(f_z1 - f_z0))
                    f_y = f_y0 + (f_y1 - f_y0) * (f_z0 - f_x0) / ((f_x1 - f_x0)-(f_z1 - f_z0))
                    f_z = f_z0 + (f_z1 - f_z0) * (f_z0 - f_x0) / ((f_x1 - f_x0)-(f_z1 - f_z0))
                elif (outCodeOut.hasBottom()):
                    f_x = f_x0 - (f_x1 - f_x0) * (f_z0 + f_y0) / ((f_y1 - f_y0)+(f_z1 - f_z0))
                    f_y = f_y0 - (f_y1 - f_y0) * (f_z0 + f_y0) / ((f_y1 - f_y0)+(f_z1 - f_z0))
                    f_z = f_z0 - (f_z1 - f_z0) * (f_z0 + f_y0) / ((f_y1 - f_y0)+(f_z1 - f_z0))
                elif (outCodeOut.hasTop()):
                    f_x = f_x0 + (f_x1 - f_x0) * (f_z0 - f_y0) / ((f_y1 - f_y0)-(f_z1 - f_z0))
                    f_y = f_y0 + (f_y1 - f_y0) * (f_z0 - f_y0) / ((f_y1 - f_y0)-(f_z1 - f_z0))
                    f_z = f_z0 + (f_z1 - f_z0) * (f_z0 - f_y0) / ((f_y1 - f_y0)-(f_z1 - f_z0))
                elif (outCodeOut.hasNear()):
                    f_x = f_x0 + (f_x1 - f_x0) * (self.perspectiveNear - f_z0) / (f_z1 - f_z0)
                    f_y = f_y0 + (f_y1 - f_y0) * (self.perspectiveNear - f_z0) / (f_z1 - f_z0)
                    f_z = self.perspectiveNear
                elif (outCodeOut.hasFar()):
                    f_x = f_x0 + (f_x1 - f_x0) * (1.0 - f_z0) / (f_z1 - f_z0)
                    f_y = f_y0 + (f_y1 - f_y0) * (1.0 - f_z0) / (f_z1 - f_z0)
                    f_z = 1.0

                if (outCodeOut.all == outCode0.all):
                    f_x0 = f_x
                    f_y0 = f_y
                    f_z0 = f_z
                    self.point0new.setPoint(f_x0, f_y0, f_z0)
                    outCode0 = self.getPerspectiveOutCode(self.point0new)
                if (outCodeOut.all == outCode1.all):
                    f_x1 = f_x
                    f_y1 = f_y
                    f_z1 = f_z
                    self.point1new.setPoint(f_x1, f_y1, f_z1)
                    outCode1 = self.getPerspectiveOutCode(self.point1new)

        return self.accept

    def calcLine(self):
        if(self.type=='parallel'):
            return self.calcParallelLine()
        if(self.type=='perspective'):
            return self.calcPerspectiveLine()

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


