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

import time
fDelay = 0.5

class Camera:
    def __init__(self,renderer):
        print(' ************************** ')
        print(' ' + str(self.__class__.__name__) + '.__init__() called')
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

        self.vrpFile = None

        self.rectangle = None
        self.text = None

        self.NDC2viewportMatrix = None
        self.viewport2screenMatrix = None
        
        self.canvasItems = []

        ## Added
        self.x01 = None
        self.y01 = None

        self.flyMatrix = np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        
    def updateTransform(self):
        self.transform.setVRP(self.vrp)
        self.transform.setVPN(self.vpn)
        self.transform.setVUP(self.vup)
        self.transform.setPRP(self.prp)

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
            

    def updateFromScene(self):
        print(' ' + str(self.__class__.__name__) + '.updateFromScene() called')

        self.lines = copy.deepcopy(self.renderer.scene.lines)
        self.points = copy.deepcopy(self.renderer.scene.world)          # World is buffer of coordinates after scale takes place
#        self.points = self.homogenize(self.renderer.scene.world)

#        print(' type(self.points) = ' + str(type(self.points)))
#        print(' self.points = ' + str(self.points))

    def updateNDC(self):
        self.transform.establishOriginMatrix()
        self.transform.establishAlignMatrix()
        if(self.type == 'parallel'):
            self.transform.establishParallelViewMatrix()
        if(self.type == 'perspective'):
            self.transform.establishPerspectiveViewMatrix()            
        self.transform.establishNDCMatrix()
        self.transform.establishNDCCoordinates()

        self.linesScreen = self.linesNDC

    def clearCamera(self):
        for c in self.canvasItems:
            if(c != None):
                self.renderer.canvas.delete(c)
        print(' self.info = ' + self.info + ' ; self.vrp = ' + str(self.vrp))

        ## Reset VRP to one from cameras file
        self.setVRP(copy.copy(self.vrpFile))
        
        self.canvasItems = []
        self.lines = None
        self.points = None
        self.linesNDC = None
        self.pointsNDC = None
        self.linesScreen = None
        self.pointsScreen = None
        
    def createCamera(self):
        print(' ' + str(self.__class__.__name__) + '.createCamera() called')

        self.setBox()
        self.updateFromScene()
        self.updateNDC()
        self.establishViewportMatrix()

        self.controller.setSize()
        self.establishScreenMatrix()
        self.establishScreenCoordinates()

        for i in range(len(self.linesScreen)):
            l = self.linesScreen[i]
            i0 = l[0]
            i1 = l[1]
            b_Draw = l[2]
            p0 = self.pointsScreen[i0]
            p1 = self.pointsScreen[i1]
            p0 = [int(self.pointsScreen[i0][0]),int(self.pointsScreen[i0][1])]
            p1 = [int(self.pointsScreen[i1][0]),int(self.pointsScreen[i1][1])]
            v_line = [p0[0],p0[1],p1[0],p1[1]]
            if(b_Draw):
                self.canvasItems.append(self.renderer.canvas.create_line(v_line, width=1.0, fill='black'))
            else:
                self.canvasItems.append(None)

#        self.debug_refreshCanvasItems()                
#        self.refreshCanvasItems()                



    def updateCamera(self):
        print(' ' + str(self.__class__.__name__) + '.updateCamera() called')
        
        self.updateFromScene()
        self.updateNDC()
#        self.establishViewportMatrix()

#        self.controller.setSize()
#        self.establishScreenMatrix()
        self.establishScreenCoordinates()
                
        self.refreshCanvasItems()

    def resizeCamera(self):

        self.setBox()
        self.controller.setSize()
        self.establishScreenMatrix()
        self.establishScreenCoordinates()
        
        self.refreshCanvasItems()


    def printSpecial(self,str_to_print,i=0):
        if(self.info=='perspective_1' and i>400):
            print(str_to_print)        

    def debug_refreshCanvasItems(self):
        print(' **** ' + str(self.__class__.__name__) + '.debug_refreshCanvasItems() called')

        self.setBox()
        for i in range(len(self.canvasItems)):
#            self.printSpecial(' ************************ ', i) 
            l = self.linesScreen[i]
            i0 = l[0]
            i1 = l[1]
            b_Draw = l[2]
            p0 = self.pointsScreen[i0]
            p1 = self.pointsScreen[i1]
            p0 = [int(self.pointsScreen[i0][0]),int(self.pointsScreen[i0][1])]
            p1 = [int(self.pointsScreen[i1][0]),int(self.pointsScreen[i1][1])]

            v_line = [p0[0],p0[1],p1[0],p1[1]]
#            v_line = [int(p0[0]),int(p0[1]),int(p1[0]),int(p1[1])]

#            self.printSpecial(' l = self.linesScreen['+str(i)+'] = ' + str(l), i)
#            if(b_Draw):
#                self.printSpecial(' b_Draw = True', i)
#            else:
#                self.printSpecial(' b_Draw = False', i)

            if(b_Draw):
#                self.printSpecial(' x = ' + str(self.x01) + ' ; y = ' + str(self.y01) + '', i)
                if(self.canvasItems[i] == None):        ## Need to draw but doesnt exist
                    self.canvasItems[i] = self.renderer.canvas.create_line(v_line, width=1.0, fill='black')
                else:                                   ## Need to draw already exists
                    self.renderer.canvas.coords(self.canvasItems[i], v_line)
            else:
#                self.printSpecial(' x = ' + str(self.x01) + ' ; y = ' + str(self.y01) + '', i)
                if(self.canvasItems[i] != None):        ## Don't draw, something that already exists
                    self.renderer.canvas.delete(self.canvasItems[i])
                    self.canvasItems[i] = None


            ## Other stuff
            if(b_Draw):
#                print(' v_line = ' + str(v_line))
                self.printSpecial(' v_line = ' + str(v_line))

                if(self.x01[0] <= p0[0] and p0[0] <= self.x01[1] and \
                   self.y01[0] <= p0[1] and p0[1] <= self.y01[1]):
                    self.printSpecial(' Draw p0 = '+str(p0)+' ', i)
                else:
                    self.printSpecial(' x = ' + str(self.x01) + ' ; y = ' + str(self.y01) + '', i)
                    self.printSpecial(' Skip p0 = '+str(p0)+' ', i)
                if(self.x01[0] <= p1[0] and p1[0] <= self.x01[1] and \
                    self.y01[0] <= p1[1] and p1[1] <= self.y01[1]):
                    self.printSpecial(' Draw p1 = '+str(p1)+' ', i)
                    print('',end='')
                else:
                    self.printSpecial(' x = ' + str(self.x01) + ' ; y = ' + str(self.y01) + '', i)
                    self.printSpecial(' Skip p1 = '+str(p1)+' ', i)

#            self.printSpecial(' ************************ ', i)

    def refreshCanvasItems(self):
        print(' ' + str(self.__class__.__name__) + '.resizeCamera() called')
        
        for i in range(len(self.canvasItems)):
            l = self.linesScreen[i]
            i0 = l[0]
            i1 = l[1]
            b_Draw = l[2]
            p0 = self.pointsScreen[i0]
            p1 = self.pointsScreen[i1]
            p0 = [int(self.pointsScreen[i0][0]),int(self.pointsScreen[i0][1])]
            p1 = [int(self.pointsScreen[i1][0]),int(self.pointsScreen[i1][1])]
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

        self.pointsScreen = (self.viewport2screenMatrix *\
                                  self.NDC2viewportMatrix) * \
                                  np.transpose(np.matrix(self.pointsNDC))

        
        self.pointsScreen = np.transpose(self.pointsScreen).tolist()

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

    def setBox(self):
        x0 = int(self.vx[0]*self.renderer.canvasWidth)
        y0 = int(self.vy[0]*self.renderer.canvasHeight)
        x1 = int(self.vx[1]*self.renderer.canvasWidth)
        y1 = int(self.vy[1]*self.renderer.canvasHeight)
        self.x01 = [x0,x1]
        self.y01 = [y0,y1]
        
    def getBox(self):
        return (self.x01, self.y01)
    def setVRP(self, vVRP):                     # Set VRP after file has been loaded
        self.vrp = vVRP
        self.transform.setVRP(self.vrp)
    def getVRP(self):
        return self.vrp
    def addInfo(self, sInfo):                   # Lines beginning with 'i'
        self.info = sInfo[0]
        return
    def addType(self, sType):                   # Lines beginning with 't'
        print(' ' + str(self.__class__.__name__) + '.addType() called')
#        sType = ['parallel']
        self.type = sType[0]
        if(self.type=='parallel'):
            self.setParallel()
        if(self.type=='perspective'):
            self.setPerspective()
        return
    def addWindow(self, lWindow):               # Lines beginning with 'w'
        self.window = lWindow
        self.wu = [lWindow[0], lWindow[1]]
        self.wv = [lWindow[2], lWindow[3]]
        self.wn = [lWindow[4], lWindow[5]]
        self.transform.setU(self.wu)
        self.transform.setV(self.wv)
        self.transform.setN(self.wn)
        if(self.type=='perspective' and self.wn != None):
            self.transform.setPerspectiveNear()
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
        self.vrpFile = copy.copy(vVRP)
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
    def setParallel(self):
        print(' ' + str(self.__class__.__name__) + '.setParallel() called')
        self.type = 'parallel'
        self.transform.setParallel()
    def setPerspective(self):
        print(' ' + str(self.__class__.__name__) + '.setPerspective() called')
        self.type = 'perspective'
        self.transform.setPerspective()
        if(self.type=='perspective' and self.wn != None):
            self.transform.setPerspectiveNear()

    def setType(self,s_type):
        print(' ' + str(self.__class__.__name__) + '.setType() called')
        self.type = s_type
        self.transform.setType(s_type)
        if(self.type=='perspective' and self.wn != None):
            self.transform.setPerspectiveNear()
            
    def establish_fly_matrix(self, i_steps=None, v_start=None, v_stop=None):
        ## Establish the fly matrix
        
        if(i_steps==None):
            i_steps = copy.copy(self.controller.flyVRPSteps)
        if(v_start==None):
            v_start = copy.copy(self.controller.flyVRPVectorA)
        if(v_stop==None):
            v_stop = copy.copy(self.controller.flyVRPVectorB)
            
        print(' Establishing translation matrix ')

        f_steps = float(i_steps)

        v_inc_fly = [1.0, 1.0, 1.0]

        v_fly = [v_stop[0]-v_start[0], v_stop[1]-v_start[1], v_stop[2]-v_start[2]]
        v_inc_fly = [1.0, 1.0, 1.0]
        v_inc_fly[0] = v_fly[0]/f_steps
        v_inc_fly[1] = v_fly[1]/f_steps
        v_inc_fly[2] = v_fly[2]/f_steps
        print(' f_steps = ' + str(f_steps))
        print(' v_fly = ' + str(v_fly))
        print(' v_inc_fly = ' + str(v_inc_fly))

        ## Establish matrix for translating all points
        m_Fly = np.matrix(\
            [[1,0,0,v_inc_fly[0]],\
             [0,1,0,v_inc_fly[1]],\
             [0,0,1,v_inc_fly[2]],\
             [0,0,0,1]])

        ## Rename translation matrix for consistancy
        self.flyMatrix = m_Fly        
