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

from Wood_Scene_05 import *
from Wood_Camera_05 import *

from tkinter import *

import time
fDelay = 0.1

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

        return

    def get(self):
        return {'cameraFileName':self.cameraFileName, 'cameras':[c.get() for c in self.cameras ], 'scene':self.scene}

    def updateScene(self):
        print(' ' + str(self.__class__.__name__) + '.updateScene() called')
        self.scene.updateScene()
        
    def updateCameras(self,iCamera=None):
        print(' ' + str(self.__class__.__name__) + '.updateCameras() called')
        if(self.scene == None):         ## Nothing to Draw
            return
        
        print(' *** Start Cycling Cameras *** ')
        if(iCamera==None):
            ## Update all
            for c in self.cameras:
                c.updateCamera()
        else:
            c = self.cameras[iCamera]
            c.updateCamera()
        print(' *** Stop Cycling Cameras *** ')

    def resizeCameras(self,iCamera=None):
        print(' ' + str(self.__class__.__name__) + '.resizeCameras() called')
        if(self.scene == None):         ## Nothing to Draw
            return
        print(' *** Start Cycling Cameras *** ')
        if(iCamera==None):
            ## Resize all
            for c in self.cameras:
                c.resizeCamera()
#                self.controller.root.update_idletasks()
#                time.sleep(fDelay)
        else:
            c = self.cameras[iCamera]
            c.resizeCamera()
#            self.controller.root.update_idletasks()
#            time.sleep(fDelay)
        print(' *** Stop Cycling Cameras *** ')

        
    def createViewports(self):
        print(' ' + str(self.__class__.__name__) + '.createViewport() called')
        self.controller.setSize()
        if(self.canvasWidth == None or self.canvasHeight == None):
            raise ValueError('Size has not been set yet')
            return

        zeroSet = False
        print(' *** Start Cycling Cameras *** ')
        for c in self.cameras:
#            x0 = c.vx[0]*self.canvasWidth
#            y0 = c.vy[0]*self.canvasHeight
#            x1 = c.vx[1]*self.canvasWidth
#            y1 = c.vy[1]*self.canvasHeight
            x0 = int(c.vx[0]*self.canvasWidth)
            y0 = int(c.vy[0]*self.canvasHeight)
            x1 = int(c.vx[1]*self.canvasWidth)
            y1 = int(c.vy[1]*self.canvasHeight)

            if(not zeroSet):
                zeroSet = True
                c.rectangle = self.canvas.create_rectangle(x0,y0,x1,y1, fill='white', tags=c.info, width=2)
            else:
                c.rectangle = self.canvas.create_rectangle(x0,y0,x1,y1, fill='white', tags=c.info, width=1)

            c.text = self.canvas.create_text(x0,y0, text=c.info, anchor=NW)
        print(' *** Stop Cycling Cameras *** ')

    def resizeViewports(self):
        print(' ' + str(self.__class__.__name__) + '.resizeViewports() called')
        if(not self.cameras):
            return
        print(' *** Start Cycling Cameras *** ')
        for c in self.cameras:
#            x0 = c.vx[0]*self.canvasWidth
#            y0 = c.vy[0]*self.canvasHeight
#            x1 = c.vx[1]*self.canvasWidth
#            y1 = c.vy[1]*self.canvasHeight
            x0 = int(c.vx[0]*self.canvasWidth)
            y0 = int(c.vy[0]*self.canvasHeight)
            x1 = int(c.vx[1]*self.canvasWidth)
            y1 = int(c.vy[1]*self.canvasHeight)

            if(c.rectangle and c.text):
                self.canvas.coords(c.rectangle,x0,y0,x1,y1)
                self.canvas.coords(c.text,x0,y0)
        print(' *** Stop Cycling Cameras *** ')
    
        
    def setSize(self,iWidth,iHeight):
        print(' ' + str(self.__class__.__name__) + '.setSize() called')
        self.canvasWidth = iWidth
        self.canvasHeight = iHeight

        self.viewport2screenMatrix = np.matrix(\
            [[float(iWidth),0,0,0],\
             [0,float(iHeight),0,0],\
             [0,0,1,0],\
             [0,0,0,1]])


    def addCamera(self, cam):
        print(' ' + str(self.__class__.__name__) + '.addCamera() called')
        if(self.scene):
            cam.scene = self.scene
        self.cameras.append(cam)
        
    def clearCameras(self):
        self.cameras = []

    def addScene(self, scn):
        self.scene = scn
        if(self.cameras):
            print(' *** Start Cycling Cameras *** ')
            for c in self.cameras:
                c.scene = scn
            print(' *** Stop Cycling Cameras *** ')
        
    def clearScene(self):
        self.scene = None

    def addObjectFile(self, sFileName):
        print(' ' + str(self.__class__.__name__) + '.addObjectFile() called')
        self.clearScene()
        oObject = Object()
        oObject.loadFile(sFileName)
        self.scene = Scene()
        self.scene.renderer = self
        self.scene.controller = self.controller
        self.scene.addObject(oObject)

        if(self.cameras):
            print(' *** Start Cycling Cameras *** ')
            for c in self.cameras:
                c.clearCamera()
                c.createCamera()
            print(' *** Stop Cycling Cameras *** ')
    
    def addCameraFile(self, sFileName):
        print(' ' + str(self.__class__.__name__) + '.addCameraFile() called')

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
                    print (' Skipping line "' + str(l_parsed) + '"  ')
            self.addCamera(cObj)                    # Add last camera        

