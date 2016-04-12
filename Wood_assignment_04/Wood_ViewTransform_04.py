# Wood, Jeff
# 100-103-5461
# 2016-04-19
# Assignment_04

#!/~/anaconda3/bin/python3.5

#   From:
#       http://stackoverflow.com/questions/15599639/whats-perfect-counterpart-in-python-for-while-not-eof
#       http://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
#       http://stackoverflow.com/questions/7118276/how-to-remove-specific-element-in-an-array-using-python
#       http://stackoverflow.com/questions/379906/parse-string-to-float-or-int
#       http://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index-in-python
#       http://docs.scipy.org/doc/numpy/reference/generated/numpy.dot.html#numpy.dot
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.vectorize.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.matrix.transpose.html
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.array.html
#
#       http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_polygon.html
#       http://zetcode.com/gui/tkinter/drawing/
#       http://effbot.org/tkinterbook/canvas.htm
#
#       https://docs.scipy.org/doc/numpy-dev/user/quickstart.html
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.array.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.matrix.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.multiply.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.matrix.transpose.html
#
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.power.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.sqrt.html
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.linalg.inv.html
#
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.sin.html
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.cos.html
#
#       http://effbot.org/pyfaq/how-do-i-copy-an-object-in-python.htm
#
#       http://codereview.stackexchange.com/questions/43928/algorithm-to-get-an-arbitrary-perpendicular-vector

import numpy as np
import copy
from numpy.linalg import inv
from numpy import linalg as LA

from Wood_Transform_04 import *
from Wood_Clipping_04 import *

class ViewTransform(Transform):
    def __init__(self, camera):
        Transform.__init__(self)

        self.camera = camera
        self.clipping = Clipping()
        
        self.step1Matrix = None
        self.step2Matrix = None
        self.step3Matrix = None
        self.step4Matrix = None
        self.step5Matrix = None
        self.step6Matrix = None

        
        self.originMatrix = None                        ## self.originMatrix = self.step1Matrix
        self.afterOriginMatrix = None                   ## self.afterOriginMatrix = self.step6Matrix * self.step5Matrix * self.step4Matrix * self.step3Matrix * self.step2Matrix
        self.viewMatrix = None                          ## self.viewMatrix = self.afterOriginMatrix
        self.world2NDCMatrix = None                     ## self.world2NDCMatrix = self.afterOriginMatrix * self.originMatrix

    def establishOriginMatrix(self):
        print(' Establishing origin matrix')

        tObj = self

        ##################################

        ## Translate VRP vector 2 origin (Step 1)
        self.step1Matrix = tObj.transformVRP2Origin(self.vVRP)

        ## Test VRP vector [0,0,0]
        mTempVRP = tObj.array2matrix(tObj.arrayAdd1(self.vVRP))
        mTempVRP = self.step1Matrix * mTempVRP
        vTempVRP = tObj.arrayRemove1(tObj.matrix2array(mTempVRP)).tolist()
        print(' vTempVRP = ',end='')
        print(vTempVRP)

        ## Combine matrices
        self.originMatrix = self.step1Matrix

    def establishAfterOriginMatrix(self):
        print(' Establishing after origin matrix ')

        tObj = self
        ##################################

        ## Rotate VPN vector 2 Z-Axis (Step 2)
        self.step2Matrix = tObj.transformVPN2Z(self.vVPN)

        ## Test new VPN vector [0,0,a]
        mTempVPN = tObj.array2matrix(tObj.arrayAdd1(self.vVPN))
        mTempVPN = self.step2Matrix * mTempVPN
        vTempVPN = tObj.arrayRemove1(tObj.matrix2array(mTempVPN)).tolist()
        print(' vTempVPN = ',end='')
        print(vTempVPN)

        ##################################
        
        ## Get new VUP vector
        mTempVUP = tObj.array2matrix(tObj.arrayAdd1(self.vVUP))
        mTempVUP = self.step2Matrix * mTempVUP
        vTempVUP = tObj.arrayRemove1(tObj.matrix2array(mTempVUP)).tolist()

        ## Rotate new VUP vector 2 YZ-Plane (Step 3)
        self.step3Matrix = tObj.transformVUP2YZ(vTempVUP)

        ## Test new VUP vector [0,b,c]
        mTempVUP = tObj.array2matrix(tObj.arrayAdd1(vTempVUP))
        mTempVUP = self.step3Matrix * mTempVUP
        vTempVUP = tObj.arrayRemove1(tObj.matrix2array(mTempVUP)).tolist()

        print(' vTempVUP = ',end='')
        print(vTempVUP)

        ##################################

        ## Shear DOP = (PRP-CW) to be prallel to Z-Axis (Step 4)
        self.step4Matrix = tObj.transformVRCshear(self.vPRP, self.vU, self.vV)

        ## Test new VUP vector [CW_x,CW_y,PRP_z]
        mTempPRP = tObj.array2matrix(tObj.arrayAdd1(self.vPRP))
        mTempPRP = self.step4Matrix * mTempPRP
        vTempPRP = tObj.arrayRemove1(tObj.matrix2array(mTempPRP)).tolist()

        print(' vTempPRP = ',end='')
        print(vTempPRP)

        ##################################

        ## Translate viewing volume to origin (Step 5)
        self.step5Matrix = tObj.transformVRCtranslate(self.vU, self.vV, self.vN)

        ## Define Center of (W)indow
        fCW_U = (self.vU[1] + self.vU[0])/2
        fCW_V = (self.vV[1] + self.vV[0])/2
        fMin_N = self.vN[0] if self.vN[0] <= self.vN[1] else self.vN[1]
        fMin_N = self.vN[0]
                
        ## Test new CW vector [0,0,0]
        mTempUVN = tObj.array2matrix(tObj.arrayAdd1([fCW_U,fCW_V,fMin_N]))
        mTempUVN = self.step5Matrix * mTempUVN
        vTempUVN = tObj.arrayRemove1(tObj.matrix2array(mTempUVN)).tolist()

        print(' vTempUVN = ',end='')
        print(vTempUVN)

        ##################################

        ## Scale viewing volume to NDC (Step 6)
        self.step6Matrix = tObj.transformVRCscale(self.vU, self.vV, self.vN)

        ##################################

        ## Combine matrices
        self.afterOriginMatrix = self.step6Matrix * self.step5Matrix * self.step4Matrix * self.step3Matrix * self.step2Matrix
        self.viewMatrix = self.afterOriginMatrix
        self.world2NDCMatrix = self.afterOriginMatrix * self.originMatrix

    def establishNDCMatrix(self):
        self.establishOriginMatrix()
        self.establishAfterOriginMatrix()
        self.world2NDCMatrix = self.afterOriginMatrix * self.originMatrix

    def establishNDCCoordinates(self):
        self.camera.linesNDC = copy.copy(self.camera.lines)
        self.camera.pointsNDC = copy.copy(self.camera.points)

        self.camera.pointsNDC = self.world2NDCMatrix * np.transpose(np.matrix(self.camera.pointsNDC))
        self.camera.pointsNDC = np.transpose(self.camera.pointsNDC)
        temp_NDC_coordinates = self.camera.pointsNDC.tolist()
                
        print('##################################')
        print('##      Clipping Occurs Here    ##')
        print('##################################')

        clipp = self.clipping

        for l in self.camera.linesNDC:
            
            index0 = l[0]
            index1 = l[1]

            # Get Previous draw state of line
            b_draw_old = l[2]
            point0 = temp_NDC_coordinates[index0]
            point1 = temp_NDC_coordinates[index1]

            clipp.setPoint0(point0[0],point0[1],point0[2])
            clipp.setPoint1(point1[0],point1[1],point1[2])

            ## Store info about whether line should be drawn
            b_draw_new = (1 if clipp.calcLine() else 0)
#            print(' i = ' + str(i) + ' ; ' + str(b_draw_new))
            l[2] = b_draw_new

            if(b_draw_new):
                point0 = clipp.getPoint0().getPointV4()
                point1 = clipp.getPoint1().getPointV4()

                temp_NDC_coordinates[index0] = point0
                temp_NDC_coordinates[index1] = point1

            
        self.camera.pointsNDC = temp_NDC_coordinates

