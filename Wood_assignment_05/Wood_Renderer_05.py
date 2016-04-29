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

import sys
import OpenGL

from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *

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
    def __init__(self, controller):
        self.cameraFileName = None
        self.cameras = []
        self.controller = controller
        self.scene = Scene()
        self.width = None
        self.height = None
        return

    def get(self):
        return {'cameraFileName':self.cameraFileName, 'cameras':[c.get() for c in self.cameras ], 'scene':self.scene}
    
        
    def addCamera(self, cam):
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
#        print(' ' + str(self.__class__.__name__) + '.' + str(sys._getframe().f_back.f_code.co_name) + '() called')
        self.scene = None

    def addObjectFile(self, sFileName):
#        print(' ' + str(self.__class__.__name__) + '.' + str(sys._getframe().f_back.f_code.co_name) + '() called')

        ## Code below is to be used to allow only a single object in scene
        ## IE each 'addObjectFile' resets and loads   
        if(self.scene.objects):
            self.clearScene()

        ## Resume normal logic                
        self.scene = Scene()
        self.scene.renderer = self
        self.scene.controller = self.controller

        oObject = Object()
        oObject.loadFile(sFileName)
        self.scene.addObject(oObject)


    def addCameraFile(self, sFileName):
#        print(' ' + str(self.__class__.__name__) + '.' + str(sys._getframe().f_back.f_code.co_name) + '() called')

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
                elif(l_type == 'e'):                # Adds VRP
                    l_parsed = vect_float(l_parsed)
                    cObj.addEye(l_parsed)
                elif(l_type == 'l'):                # Adds VPN
                    l_parsed = vect_float(l_parsed)
                    cObj.addLookAt(l_parsed)
                elif(l_type == 'u'):                # Adds VUP
                    l_parsed = vect_float(l_parsed)
                    cObj.addUp(l_parsed)
                else:
                    print (' Skipping line "' + str(l_parsed) + '"  ')
            self.addCamera(cObj)                    # Add last camera        


