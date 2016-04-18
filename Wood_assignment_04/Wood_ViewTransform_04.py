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
        print(' ' + str(self.__class__.__name__) + '.__init__() called')

        Transform.__init__(self)

        self.camera = camera
        self.clipping = Clipping(camera)

        self.type = 'parallel'
        
        self.step1Matrix = None
        self.step2Matrix = None
        self.step3Matrix = None
        self.step4Matrix = None
        self.step5Matrix = None
        self.step6Matrix = None

        self.step7Matrix = None
        
        self.originMatrix = None                        ## self.originMatrix = self.step1Matrix
        self.alignMatrix = None                         ## self.alignMatrix = self.step3Matrix * self.step2Matrix
        self.viewMatrix = None                          ## self.viewMatrix = self.step6Matrix * self.step5Matrix * self.step4Matrix
        self.world2NDCMatrix = None                     ## self.world2NDCMatrix = self.viewMatrix * self.alignMatrix * self.originMatrix

        
    def setParallel(self):
        print(' ' + str(self.__class__.__name__) + '.setParallel() called')
        self.type = 'parallel'
        self.clipping.setParallel()
    def setPerspective(self):
        print(' ' + str(self.__class__.__name__) + '.setPerspective() called')
        self.type = 'perspective'
        self.clipping.setPerspective()
    def setType(self,s_type):
        print(' ' + str(self.__class__.__name__) + '.setType() called')
        self.type = s_type
        self.clipping.setType(s_type)

    def homogenize(self,list_to_convert):

        l_return = []
        for i in range(len(list_to_convert)):
            l = list_to_convert[i]
            if(len(l) != 4):
                raise ValueError(' List does not contain vectors of length 4')
            else:
                f_last = l[3]
                v_append = [l[0] / f_last, l[1] / f_last, l[2] / f_last, 1]
                l_return.append(v_append)
        return l_return
    
    def establishOriginMatrix(self):
        print(' Establishing Origin matrix')

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

    def establishAlignMatrix(self):
        print(' Establishing Align matrix ')

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

        ## Combine matrices
        self.alignMatrix = self.step3Matrix * self.step2Matrix

    def establishParallelViewMatrix(self):
        print(' Establishing Parallel View matrix ')

        tObj = self
        ##################################
        
        ## Shear DOP = (PRP-CW) to be prallel to Z-Axis (Step 4)
        self.step4Matrix = tObj.transformVRCshear(self.vPRP, self.vU, self.vV)

        ## Test new PRP vector [CW_x,CW_y,PRP_z]
        mTempPRP = tObj.array2matrix(tObj.arrayAdd1(self.vPRP))
        mTempPRP = self.step4Matrix * mTempPRP
        vTempPRP = tObj.arrayRemove1(tObj.matrix2array(mTempPRP)).tolist()

        print(' vTempPRP = ',end='')
        print(vTempPRP)

        ##################################

        ## Translate viewing volume to origin (Step 5)
        self.step5Matrix = tObj.transformVRCtranslate_DimUVN(self.vU, self.vV, self.vN)

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
        self.step6Matrix = tObj.transformVRCscale_DimUVN(self.vU, self.vV, self.vN)

        ##################################

        ## Combine matrices
        self.viewMatrix = self.step6Matrix * self.step5Matrix * self.step4Matrix
#        self.world2NDCMatrix = self.viewMatrix * self.alignMatrix * self.originMatrix

    def establishPerspectiveViewMatrix(self):
        print(' Establishing Perspective View matrix ')

        tObj = self
        ##################################
        
        ## Translate PRP to origin (Step 4)
        self.step4Matrix = tObj.transformVRCtranslate_PRP(self.vPRP)

        ## Test new PRP vector [CW_x,CW_y,PRP_z]
        mTempPRP = tObj.array2matrix(tObj.arrayAdd1(self.vPRP))
        mTempPRP = self.step4Matrix * mTempPRP
        vTempPRP = tObj.arrayRemove1(tObj.matrix2array(mTempPRP)).tolist()

        print(' vTempPRP = ',end='')
        print(vTempPRP)

        ## Test new PRP vector [CW_x,CW_y,PRP_z]
        mTempVRP = tObj.array2matrix(tObj.arrayAdd1(self.vVRP))
        mTempVRP = self.step4Matrix * mTempVRP
        vTempVRP = tObj.arrayRemove1(tObj.matrix2array(mTempVRP)).tolist()

        print(' vTempVRP = ',end='')
        print(vTempVRP)

        ## VRP Vector should now be 0 fom step 1 (BEFORE steps below)
        ## Test new VRP vector which will get used in step 6
        vNewVRP = tObj.array2matrix(tObj.arrayAdd1([0,0,0]))
        mNewVRP = self.step4Matrix * vNewVRP
        vNewVRP = tObj.arrayRemove1(tObj.matrix2array(mNewVRP)).tolist()

        print(' vNewVRP = ',end='')
        print(vNewVRP)

        ## PRP Vector should now be 0 from step 4 (AFTER STEPS below)
        ## Test new PRP vector for completeness
        vNewPRP = tObj.array2matrix(tObj.arrayAdd1(self.vPRP))
        mNewPRP = self.step4Matrix * vNewPRP
        vNewPRP = tObj.arrayRemove1(tObj.matrix2array(mNewPRP)).tolist()

        print(' vNewPRP = ',end='')
        print(vNewPRP)
        
        ##################################

        ## Shear DOP = (PRP-CW) to be prallel to Z-Axis (Step 5)
        self.step5Matrix = tObj.transformVRCshear(self.vPRP, self.vU, self.vV)

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
        self.step6Matrix = tObj.transformVRCscale_DimUVN_VRPz(self.vU, self.vV, self.vN, vNewVRP)

        ##################################

        ## Transform frustum back to NDC (Step 7)
        self.step7Matrix = tObj.transformFrustum(self.vN, self.vPRP)
                
        ## Test new PerspectiveNear
        mTemp = tObj.array2matrix(tObj.arrayAdd1([0,0,self.perspectiveNear]))
        mTemp = self.step7Matrix * mTempUVN
        vTemp = tObj.arrayRemove1(tObj.matrix2array(mTempUVN)).tolist()

        print(' vTemp = ',end='')
        print(vTemp)

        ##### Lines below should be toggled for correct perspective clipping #####
        ## Perspective clipping using Frustum
        self.step7Matrix = np.matrix(np.eye(4))

        ##################################

        ## Combine matrices
        self.viewMatrix = self.step7Matrix * self.step6Matrix * self.step5Matrix * self.step4Matrix
#        self.world2NDCMatrix = self.viewMatrix * self.alignMatrix * self.originMatrix

    def establishNDCMatrix(self):

#        self.establishOriginMatrix()
#        self.establishAlignMatrix()
#        self.establishViewMatrix()

        self.world2NDCMatrix = self.viewMatrix * self.alignMatrix * self.originMatrix
        
    def establishNDCCoordinates(self):

        self.camera.linesNDC = copy.copy(self.camera.lines)
        self.camera.pointsNDC = copy.copy(self.camera.points)

        self.camera.pointsNDC = self.world2NDCMatrix * np.transpose(np.matrix(self.camera.pointsNDC))
        self.camera.pointsNDC = np.transpose(self.camera.pointsNDC).tolist()

        ##### Lines below should be toggled for correct perspective clipping #####
        ## Perspective clipping using Frustum
        temp_NDC_coordinates = self.camera.pointsNDC
        ## Perspective clipping using NDC
#        temp_NDC_coordinates = self.homogenize(self.camera.pointsNDC)
        
        print('##################################')
        print('##      Clipping Occurs Here    ##')
        print('##################################')

        clipp = self.clipping

        ##### Lines below should be toggled for correct perspective clipping #####
        ## Perspective clipping using NDC

        for l in self.camera.linesNDC:
            
            index0 = l[0]
            index1 = l[1]

            # Get Previous draw state of line
            b_draw_old = l[2]
            point0 = temp_NDC_coordinates[index0]
            point1 = temp_NDC_coordinates[index1]

            clipp.setPoint0(point0[0], point0[1], point0[2], point0[3])
            clipp.setPoint1(point1[0], point1[1], point1[2], point1[3])

            ## Store info about whether line should be drawn
            b_draw_new = (1 if clipp.calcLine() else 0)
            l[2] = b_draw_new

            if(b_draw_new):
                temp_point0 = clipp.getPoint0().getPointV4()
                temp_point1 = clipp.getPoint1().getPointV4()

                ##### Lines below should be toggled for correct perspective clipping #####
                ## Perspective clipping using Frustum                
                point0 = [temp_point0[0]/temp_point0[3], temp_point0[1]/temp_point0[3], temp_point0[2]/temp_point0[3], 1]
                point1 = [temp_point1[0]/temp_point1[3], temp_point1[1]/temp_point1[3], temp_point1[2]/temp_point1[3], 1]
                ## Perspective clipping using NDC
#                point0 = temp_point0
#                point1 = temp_point1

                temp_NDC_coordinates[index0] = point0
                temp_NDC_coordinates[index1] = point1

            
        self.camera.pointsNDC = temp_NDC_coordinates

