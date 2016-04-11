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
from Wood_Camera_04 import *

from tkinter import *

def vect_int(arr):
    rtrn = []
    for k in arr:
        rtrn.append(int(k))
    return rtrn

def vect_float(arr):
    rtrn = []
    for k in arr:
        rtrn.append(float(k))
    return rtrn

class Renderer():
    def __init__(self):
        self.cameraFileName = None
        self.cameras = []
        self.canvas = None
        self.controller = None
        self.scene = None
        self.canvasWidth = None
        self.canvasHeight = None
        self.viewport2screenMatrix = None
        self.addCamera('cameras_04.txt')

        return

    def get(self):
        return {'cameraFileName':self.cameraFileName, 'cameras':[c.get() for c in self.cameras ], 'scene':self.scene}
    def createRender(self):
        
        return
    def updateRender(self,iCamera=None):
        self.scene.updateScene()
        if(iCamera==None):
            ## Update all
            for c in self.cameras:
                c.updateCamera()
        else:
            c = self.cameras[iCamera]
            c.updateCamera()
    def createViewports(self):
        self.controller.setSize()
        if(self.canvasWidth == None or self.canvasHeight == None):
            raise ValueError('Size has not been set yet')
            return
        print(' self.canvasHeight = ' + str(self.canvasHeight))
        print(' self.canvasWidth = ' + str(self.canvasWidth))
              
        print(' self.cameras count = ' + str(len(self.cameras)))
        zeroSet = False
        for c in self.cameras:
            x0 = c.vx[0]*self.canvasWidth
            y0 = c.vy[0]*self.canvasHeight
            x1 = c.vx[1]*self.canvasWidth
            y1 = c.vy[1]*self.canvasHeight
            print(' c.vx = ' + str(c.vx))
            print(' c.vy = ' + str(c.vy))
            print(' [x0,y0] = ' + str([x0,y0]) + ' ; [x1,y1] = ' + str([x1,y1]))

            if(not zeroSet):
                zeroSet = True
                c.rectangle = self.controller.canvas.create_rectangle(x0,y0,x1,y1, fill='white', tags=c.info, width=2)
            else:
                c.rectangle = self.controller.canvas.create_rectangle(x0,y0,x1,y1, fill='white', tags=c.info, width=1)

            c.text = self.controller.canvas.create_text(x0,y0, text=c.info, anchor=NW)
            self.controller.canvas.update()

    def refreshViewports(self):

        if(len(self.cameras)==0):
            return

        for c in self.cameras:
            x0 = c.vx[0]*self.canvasWidth
            y0 = c.vy[0]*self.canvasHeight
            x1 = c.vx[1]*self.canvasWidth
            y1 = c.vy[1]*self.canvasHeight
            if(c.rectangle and c.text):
                print(' c.vx = ' + str(c.vx))
                print(' c.vy = ' + str(c.vy))
                print(' [x0,y0] = ' + str([x0,y0]) + ' ; [x1,y1] = ' + str([x1,y1]))
                print(' c.rectangle = ' + str(c.rectangle))
                print(' c.text = ' + str(c.text))
            
                self.controller.canvas.coords(c.rectangle,x0,y0,x1,y1)
                self.controller.canvas.coords(c.text,x0,y0)
    
        
    def setSize(self,iWidth,iHeight):

        self.canvasWidth = iWidth
        self.canvasHeight = iHeight

        self.viewport2screenMatrix = np.matrix(\
            [[float(iWidth),0,0,0],\
             [0,float(iHeight),0,0],\
             [0,0,1,0],\
             [0,0,0,1]])


    def addCamera(self, cam):
        self.cameras.append(cam)
        
    def clearCameras(self):
        self.cameras = []

    def addScene(self, scn):
        self.scene = scn
        
    def clearScene(self):
        self.scene = None

    def addObjectFile(self, sFileName):
        self.clearScene()
        oObject = Object()
        oObject.loadFile(sFileName)
        self.scene = Scene()
        self.scene.addObject(oObject)

        if(self.cameras):
            for c in self.cameras:
                c.createCamera()
    
    def addCameraFile(self, sFileName):
        self.cameraFileName = sFileName
        self.clearCameras()
        
        cObj = None
        with open(sFileName) as openCameraFile:
            print(' sFileName = ' + str(sFileName))

            for l in openCameraFile:
                l_parsed = l.split()
                l_type = l_parsed[0]
                l_parsed.pop(0)
                if(l_type == 'c'):                  # Adds new camera
                    if(cObj != None):               # If there is already a camera
                        self.addCamera(cObj)        # Add it before you -- 
                    cObj = Camera(self)             # Create a new camera
                elif(l_type == 'i'):                # Adds info
                    cObj.addInfo(l_parsed)
                elif(l_type == 't'):                # Adds type
                    cObj.addType(l_parsed)
                elif(l_type == 'w'):                # Adds window
                    l_parsed = vect_float(l_parsed)
                    cObj.addWindow(l_parsed)
                elif(l_type == 's'):                # Adds viewport
                    l_parsed = vect_float(l_parsed)
                    cObj.addViewport(l_parsed)
                elif(l_type == 'r'):                # Adds VRP
                    l_parsed = vect_float(l_parsed)
                    cObj.addVRP(l_parsed)
                elif(l_type == 'n'):                # Adds VPN
                    l_parsed = vect_float(l_parsed)
                    cObj.addVPN(l_parsed)
                elif(l_type == 'u'):                # Adds VUP
                    l_parsed = vect_float(l_parsed)
                    cObj.addVUP(l_parsed)
                elif(l_type == 'p'):                # Adds PRP
                    l_parsed = vect_float(l_parsed)
                    cObj.addPRP(l_parsed)
                else:
                    raise ValueError(' "' + str(l_type) + '" Not valid ')
            self.addCamera(cObj)                    # Add last camera
                    



