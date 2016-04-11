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

from Wood_Camera_04 import *

class Renderer():
    def __init__(self):
        self.cameraFileName = None
        self.cameras = []
        self.scenes = []

        return

    def get(self):
        return {'cameraFileName':self.cameraFileName, 'cameras':[c.get() for c in self.cameras ], 'scenes':[s.get() for s in self.cameras]}

    def addCamera(self, cam):
        self.cameras.append(cam)
        
    def clearCameras(self):
        self.cameras = []

    def addScene(self, scn):
        self.scenes.append(scn)
        
    def clearScenes(self):
        self.scenes = []
        
    def loadFile(self, sFileName):
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
                    cObj = Camera()                 # Create a new camera
                elif(l_type == 'i'):                # Adds info
                    cObj.addInfo(l_parsed)
                elif(l_type == 't'):                # Adds type
                    cObj.addType(l_parsed)
                elif(l_type == 'w'):                # Adds window
                    cObj.addWindow(l_parsed)
                elif(l_type == 's'):                # Adds viewport
                    cObj.addViewport(l_parsed)
                elif(l_type == 'r'):                # Adds VRP
                    cObj.addVRP(l_parsed)
                elif(l_type == 'n'):                # Adds VPN
                    cObj.addVPN(l_parsed)
                elif(l_type == 'u'):                # Adds VUP
                    cObj.addVUP(l_parsed)
                elif(l_type == 'p'):                # Adds PRP
                    cObj.addPRP(l_parsed)
                else:
                    raise ValueError(' "' + str(l_type) + '" Not valid ')
            self.addCamera(cObj)                    # Add last camera
                    



