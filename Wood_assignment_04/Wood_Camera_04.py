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
        self.viewport2screenMatrix = None
        
        self.canvasItems = []

    def updateTransform(self):
        self.transform.setVRP(self.vrp)
        self.transform.setVPN(self.vpn)
        self.transform.setVUP(self.vup)
        self.transform.setPRP(self.prp)

    def updateFromScene(self):
        print(' ' + str(self.__class__.__name__) + '.getFromScene() called')
        self.renderer.updateScene()
        self.scene = self.renderer.scene
        self.lines = copy.copy(self.renderer.scene.lines)
        self.points = copy.copy(self.renderer.scene.world)          # World is buffer of coordinates after scale takes place

    def updateNDC(self):
        self.transform.establishOriginMatrix()
        self.transform.establishAfterOriginMatrix()
        self.transform.establishNDCMatrix()
        self.transform.establishNDCCoordinates()

    def clearCamera(self):
        for c in self.canvasItems:
            if(c != None):
                self.renderer.canvas.delete(c)
        self.canvasItems = []
        self.lines = None
        self.points = None
        self.linesNDC = None
        self.pointsNDC = None
        self.linesScreen = None
        self.pointsScreen = None
        
    def createCamera(self):
        print(' ' + str(self.__class__.__name__) + '.createCamera() called')
        
        self.updateFromScene()
        self.updateNDC()
        self.establishViewportMatrix()

        self.controller.setSize()
        self.establishScreenMatrix()
        self.establishScreenCoordinates()       

        for l in self.linesScreen:
            i0 = l[0]
            i1 = l[1]
            b_Draw = l[2]
            p0 = self.pointsScreen[i0]
            p1 = self.pointsScreen[i1]
            v_line = [p0[0],p0[1],p1[0],p1[1]]
            if(b_Draw):
                self.canvasItems.append(self.renderer.canvas.create_line(v_line, width=1.0, fill='black'))
            else:
                self.canvasItems.append(None)

    def getSpecial(self):
        if(self.info[0]=='perspective_1'):
            print(' ************************ ')
            print(' self.vrp = ' + str(self.vrp))

#            print(' self.transform.originMatrix = ')
#            print(str(self.transform.originMatrix))
#            print('\n')

            print(' self.transform.afterOriginMatrix = ')
            print(str(self.transform.afterOriginMatrix))
            print('\n')

            print(' self.transform.step2Matrix = ')
            print(str(self.transform.step2Matrix))
            print('\n')

            print(' self.transform.step3Matrix = ')
            print(str(self.transform.step3Matrix))
            print('\n')

            print(' self.transform.step4Matrix = ')
            print(str(self.transform.step4Matrix))
            print('\n')

            print(' self.transform.step5Matrix = ')
            print(str(self.transform.step5Matrix))
            print('\n')

            print(' self.transform.step6Matrix = ')
            print(str(self.transform.step6Matrix))
            print('\n')

#            print(' self.transform.world2NDCMatrix = ')
#            print(str(self.transform.world2NDCMatrix))
#            print('\n')
            
            
#            print(' self.NDC2viewportMatrix = ')
#            print(str(self.NDC2viewportMatrix))
#            print('\n')

#            print(' self.viewport2screenMatrix = ')
#            print(str(self.viewport2screenMatrix))
#            print('\n')
            
            print(' ************************ ')

    def updateCamera(self):
        print(' ' + str(self.__class__.__name__) + '.updateCamera() called')
        
        self.updateFromScene()
        self.updateNDC()
        self.establishViewportMatrix()

        self.controller.setSize()
        self.establishScreenMatrix()
        self.establishScreenCoordinates()
                
        self.refreshCanvasItems()

    def resizeCamera(self):
        
        self.controller.setSize()
        self.establishScreenMatrix()
        self.establishScreenCoordinates()

        self.refreshCanvasItems()

    def refreshCanvasItems(self):
        print(' ' + str(self.__class__.__name__) + '.resizeCamera() called')
        
        for i in range(len(self.canvasItems)):
            l = self.linesScreen[i]
            i0 = l[0]
            i1 = l[1]
            b_Draw = l[2]
            p0 = self.pointsScreen[i0]
            p1 = self.pointsScreen[i1]
            v_line = [p0[0],p0[1],p1[0],p1[1]]
            if(b_Draw):
                if(self.canvasItems[i] == None):        ## Need to draw but doesnt exist
                    self.canvasItems[i] = self.renderer.canvas.create_line(v_line, width=1.0, fill='black')
                else:                                   ## Need to draw already exists
                    self.renderer.canvas.coords(self.canvasItems[i], v_line)
            else:
                if(self.canvasItems[i] != None):        ## Don't draw, something that already exists
                    self.renderer.canvas.delete(self.canvasItems[i])
                    self.canvasItems[i] = None

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
        self.transform.setN(self.wn)

        return
    def addViewport(self, lViewport):           # Lines beginning wtih 's'
        self.viewport = lViewport
        self.vx = [lViewport[0], lViewport[2]]
        self.vy = [lViewport[1], lViewport[3]]
        return
    def addVRP(self, vVRP):                     # Lines beginning with 'r'
        self.vrp = vVRP
        self.vrpA = copy.copy(vVRP)
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
        print(' ' + str(self.__class__.__name__) + '.establishScreenMatrix() called')
        print(' Establishing Screen matrix ')
        iWidth = self.renderer.canvasWidth
        iHeight = self.renderer.canvasHeight
        self.viewport2screenMatrix = np.matrix(\
            [[float(iWidth),0,0,0],\
             [0,float(iHeight),0,0],\
             [0,0,1,0],\
             [0,0,0,1]])

    def establishScreenCoordinates(self):
        print(' ' + str(self.__class__.__name__) + '.establishScreenCoordinates() called')
        print(' Establishing Screen coordinates ')
        # Transform vertices into coordinates

        self.linesScreen = copy.copy(self.linesNDC)
        self.pointsScreen = (self.viewport2screenMatrix *\
                                  self.NDC2viewportMatrix) * \
                                  np.transpose(np.matrix(self.pointsNDC))

        
        self.pointsScreen = np.transpose(self.pointsScreen).tolist()
