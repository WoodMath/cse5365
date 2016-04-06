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
from wood_transform_03 import *
from wood_clipping_03 import *

from Wood_Camera_04 import *

class Renderer():
    def __init__(self):
        self.cameras = []

        return

    def addCamera(self, cam):
        self.cameras.append(cam)
        
    def clearCameras(self):
        self.cameras = []

    def loadFile(self,sFileName):
        self.cameraFileName = sFileName

        cObj = None
        with open(sFileName) as openCameraFile:
            print(' sFileName = ' + str(sFileName))
            for l in openObjectFile:
                l_parsed = l.split()
                l_type = l_parsed[0]
                l_parsed.pop(0)
                if(l_type == 'c'):                  # Adds new camera
                    return
                elif(l_type == 'i'):                # Adds info
                    return
                elif(l_type == 't'):                # Adds type
                    return
                elif(l_type == 'w'):                # Adds window
                    return
                elif(l_type == 's'):                # Adds viewport
                    return
                elif(l_type == 'r'):                # Adds VRP
                    return
                elif(l_type == 'n'):                # Adds VPN
                    return
                elif(l_type == 'u'):                # Adds VUP
                    return
                elif(l_type == 'p'):                # Adds PRP
                    return
                else
                    raise ValueError(' "' + str(l_type) + '" Not valid ')
                    


r = Renderer()
