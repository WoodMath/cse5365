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

from Wood_ViewTransform_04 import *
    
class Camera:
    def __init__(self,renderer):
        self.renderer = renderer
        self.controller = renderer.controller
        self.cameraFileName = []
        self.scene = None

        self.lines = None
        self.points = None
        self.linesNDC = None
        self.pointsNDC = None
        self.linesScreen = None
        self.pointsScreen = None

        self.transform = ViewTransform(self)

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

        self.rectangle = None
        self.text = None

        self.NDC2viewportMatrix = None

    def updateTransform(self):
        self.transform.setVRP(self.vrp)
        self.transform.setVPN(self.vpn)
        self.transform.setVUP(self.vup)
        self.transform.setPRP(self.prp)

    def getFromScene(self):
        self.renderer.updateScene()
        self.scene = self.renderer.scene
        self.lines = copy.copy(self.renderer.scene.lines)
        self.points = copy.copy(self.renderer.scene.world)          # World is buffer of coordinates after scale takes place

    def updateNDC(self):
        self.transform.establishOriginMatrix()
        self.transform.establishAfterOriginMatrix()
        self.transform.establishNDCMatrix()
        self.transform.establishNDCCoordinates()
        
    def updateScreen(self):
        self.establishViewportMatrix()
        self.establishScreenMatrix()
        self.establishScreenCoordinates()
        
    def createCamera(self):
        self.getFromScene()
        self.updateNDC()
        self.updateScreen()
        
    def updateCamera(self):
        self.getFromScene()
        self.updateNDC()
        self.updateScreen()        

    def get(self):
        return {'cameraFileName':self.cameraFileName, \
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

    def setVRP(self, vVRP):                     # Set VRP after file has been loaded
        self.vrp = vVRP
        self.transform.setVRP(self.vrp)
        
    def addInfo(self, sInfo):                   # Lines beginning with 'i'
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
        self.transform.setU(self.wu)
        self.transform.setV(self.wv)
        self.transform.setV(self.wn)

        return
    def addViewport(self, lViewport):           # Lines beginning wtih 's'
        self.viewport = lViewport
        self.vx = [lViewport[0], lViewport[2]]
        self.vy = [lViewport[1], lViewport[3]]
        return
    def addVRP(self, vVRP):                     # Lines beginning with 'r'
        self.vrp = vVRP
        self.vrpA = vVRP
        self.vrpB = [1,1,1]
        self.transform.setVRP(self.vrp)
        return
    def addVPN(self, vVPN):                     # Lines beginning with 'n'
        self.vpn = vVPN
        self.transform.setVPN(self.vpn)
        return
    def addVUP(self, vVUP):                     # Lines beginning with 'u'
        self.vup = vVUP
        self.transform.setVUP(self.vup)
        return
    def addPRP(self, vPRP):                     # Lines beginning with 'p'
        self.prp = vPRP
        self.transform.setPRP(self.prp)
        return
       
    def establishViewportMatrix(self):
        print(' Establishing viewport matrix ')

        tObj = self.transform
        self.sx = (self.vx[1]-self.vx[0])/(tObj.vNDCx[1]-tObj.vNDCx[0])
        self.sy = (self.vy[1]-self.vy[0])/(tObj.vNDCy[1]-tObj.vNDCy[0])

        wMat=np.matrix(\
            [[1,0,0,-self.wu[0]],\
             [0,-1,0,self.wv[1]],\
             [0,0,1,-self.wn[0]],\
             [0,0,0,1]])

        wMat=np.matrix(\
            [[1,0,0,-tObj.vNDCx[0]],\
             [0,-1,0,tObj.vNDCy[1]],\
             [0,0,1,-tObj.vNDCz[0]],\
             [0,0,0,1]])
        sMat=np.matrix(\
            [[self.sx,0,0,0],\
             [0,self.sy,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        vMat=np.matrix(\
            [[1,0,0,self.vx[0]],\
             [0,1,0,self.vy[0]],\
             [0,0,1,0],\
             [0,0,0,1]])

        self.NDC2viewportMatrix = vMat * sMat * wMat;

    def establishScreenMatrix(self):
        print(' Establishing Screen matrix ')
        iWidth = self.renderer.canvasWidth
        iHeight = self.renderer.canvasHeight
        self.viewport2screenMatrix = np.matrix(\
            [[float(iWidth),0,0,0],\
             [0,float(iHeight),0,0],\
             [0,0,1,0],\
             [0,0,0,1]])

    def establishScreenCoordinates(self):
        print(' Establishing Screen coordinates ')
        # Transform vertices into coordinates

        self.linesScreen = copy.copy(self.linesNDC)
        self.pointsScreen = self.viewport2screenMatrix *\
                                  self.NDC2viewportMatrix * \
                                  np.transpose(np.matrix(self.pointsNDC))

        
        self.pointsScreen = np.transpose(self.pointsScreen).tolist()
