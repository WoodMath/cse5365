# Wood, Jeff
# 100-103-5461
# 2016-04-19
# Assignment_04

#   From
#       http://www.jesshamrick.com/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/
#       http://stackoverflow.com/questions/1607612/python-how-do-i-make-a-subclass-from-a-superclass
#       http://jfine-python-classes.readthedocs.org/en/latest/subclass-int.html
#       https://docs.python.org/3.5/tutorial/classes.html
#       https://docs.python.org/2/tutorial/classes.html
#       http://learnpythonthehardway.org/book/ex44.html

import numpy as np
import copy
from numpy.linalg import inv
from numpy import linalg as LA

from Wood_Scene_04 import *
    
class Camera:
    def __init__(self):
        self.scenes = []
        self.cameraFileName = []

        ## tags from 'camera' file
        self.info = None
        self.type = None
        self.vrp = None
        self.vpn = None
        self.vup = None
        self.prp = None
        self.window = None
        self.viewport = None

        ## tags below derived from 'self.window' and 'self.viewport' defined above
        self.wu = None
        self.wv = None
        self.wn = None
        self.vx = None
        self.vy = None

        self.vrpA = None
        self.vrpB = None

        self.flyMatrix = np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])

        return

    def get(self):
        return {'scenes':self.scenes, \
                'cameraFileName':self.cameraFileName, \
                'info':self.info, \
                'type':self.type, \
                'VRP':self.vrp, \
                'VPN':self.vpn, \
                'VUP':self.vup, \
                'PRP':self.prp, \
                'window':self.window, \
                'viewport':self.viewport, \
                'wU':self.wu, \
                'wV':self.wv, \
                'wN':self.wn, \
                'vX':self.vx, \
                'vY':self.vy}

    def addScene(self, scn):
        self.scenes.append(scn)
        
    def clearScenes(self):
        self.scenes = []
    def addInfo(self, sInfo):                  # Lines beginning with 'i'
        self.info = sInfo
        return
    def addType(self, sType):                   # Lines beginning with 't'
        self.type = sType
        return
    def addWindow(self, lWindow):               # Lines beginning with 'w'
        self.window = lWindow
        self.wu = [lWindow[0], lWindow[1]]
        self.wv = [lWindow[2], lWindow[3]]
        self.wn = [lWindow[4], lWindow[5]]
        return
    def addViewport(self, lViewport):           # Lines beginning wtih 's'
        self.viewport = lViewport
        self.vx = [lViewport[0], lViewport[1]]
        self.vy = [lViewport[2], lViewport[3]]
        return
    def addVRP(self, vVRP):                     # Lines beginning with 'r'
        self.vrp = vVRP
        self.vrpA = vVRP
        self.vrpB = [0,0,0]
        return
    def addVPN(self, vVPN):                     # Lines beginning with 'n'
        self.vpn = vVPN
        return
    def addVUP(self, vVUP):                     # Lines beginning with 'u'
        self.vup = vVUP
        return
    def addPRP(self, vPRP):                     # Lines beginning with 'p'
        self.prp = vPRP
        return
       


    def establish_origin_matrix(self):
        print(' Establishing origin matrix')

        tObj = self.view_transform

        ##################################

        ## Translate VRP vector 2 origin (Step 1)
        self.step1Matrix = tObj.transformVRP2Origin(self.vrp)

        ## Test VRP vector [0,0,0]
        mTempVRP = tObj.array2matrix(tObj.arrayAdd1(self.vrp))
        mTempVRP = self.step1Matrix * mTempVRP
        vTempVRP = tObj.arrayRemove1(tObj.matrix2array(mTempVRP))
        print(' vTempVRP = ',end='')
        print(vTempVRP)

        ## Combine matrices
        self.originMatrix = self.step1Matrix

    def establish_after_origin_matrix(self):
        print(' Establishing after origin matrix ')

        tObj = self.view_transform
        ##################################

        ## Rotate VPN vector 2 Z-Axis (Step 2)
        self.step2Matrix = tObj.transformVPN2Z(self.vpn)

        ## Test new VPN vector [0,0,a]
        mTempVPN = tObj.array2matrix(tObj.arrayAdd1(self.vpn))
        mTempVPN = self.step2Matrix * mTempVPN
        vTempVPN = tObj.arrayRemove1(tObj.matrix2array(mTempVPN))
        print(' vTempVPN = ',end='')
        print(vTempVPN)

        ##################################
        
        ## Get new VUP vector
        mTempVUP = tObj.array2matrix(tObj.arrayAdd1(self.vup))
        mTempVUP = self.step2Matrix * mTempVUP
        vTempVUP = tObj.arrayRemove1(tObj.matrix2array(mTempVUP))

        ## Rotate new VUP vector 2 YZ-Plane (Step 3)
        self.step3Matrix = tObj.transformVUP2YZ(vTempVUP)

        ## Test new VUP vector [0,b,c]
        mTempVUP = tObj.array2matrix(tObj.arrayAdd1(vTempVUP))
        mTempVUP = self.step3Matrix * mTempVUP
        vTempVUP = tObj.arrayRemove1(tObj.matrix2array(mTempVUP))

        print(' vTempVUP = ',end='')
        print(vTempVUP)

        ##################################

        ## Define (W)indowed view volume
        v_Dim_U = self.wu
        v_Dim_V = self.wv
        v_Dim_N = self.wn

        ## Shear DOP = (PRP-CW) to be prallel to Z-Axis (Step 4)
        self.step4Matrix = tObj.transformVRCshear(self.prp,v_Dim_U,v_Dim_V)

        ## Test new VUP vector [CW_x,CW_y,PRP_z]
        mTempPRP = tObj.array2matrix(tObj.arrayAdd1(self.prp))
        mTempPRP = self.step4Matrix * mTempPRP
        vTempPRP = tObj.arrayRemove1(tObj.matrix2array(mTempPRP))

        print(' vTempPRP = ',end='')
        print(vTempPRP)

        ##################################

        ## Translate viewing volume to origin (Step 5)
        self.step5Matrix = tObj.transformVRCtranslate(v_Dim_U,v_Dim_V,v_Dim_N)

        ## Define Center of (W)indow
        fCW_U = (v_Dim_U[1]+v_Dim_U[0])/2
        fCW_V = (v_Dim_V[1]+v_Dim_V[0])/2
        fMin_N = v_Dim_N[0] if v_Dim_N[0] <= v_Dim_N[1] else v_Dim_N[1]
        fMin_N = v_Dim_N[0]
                
        ## Test new CW vector [0,0,0]
        mTempUVN = tObj.array2matrix(tObj.arrayAdd1([fCW_U,fCW_V,fMin_N]))
        mTempUVN = self.step5Matrix * mTempUVN
        vTempUVN = tObj.arrayRemove1(tObj.matrix2array(mTempUVN))

        print(' vTempUVN = ',end='')
        print(vTempUVN)

        ##################################

        ## Scale viewing volume to NDC (Step 6)
        self.step6Matrix = tObj.transformVRCscale(v_Dim_U,v_Dim_V,v_Dim_N)

        ##################################

        self.viewMatrix = self.step6Matrix * self.step5Matrix * self.step4Matrix * self.step3Matrix * self.step2Matrix

        self.world2NDCMatrix = self.viewMatrix * self.originMatrix
