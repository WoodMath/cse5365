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

        return

    def addScene(self, scn):
        self.scenes.append(scn)
        
    def clearScenes(self):
        self.scenes = []


    def add_window(self):       # Lines beginning with 'w'
        return
    def add_viewport(self):     # Lines beginning wtih 's'
        return
    def add_vrp(self):          # Lines beginning with 'r'
        return
    def add_vpn(self):          # Lines beginning with 'n'
        return
    def add_vup(self):          # Lines beginning with 'u'
        return
    def add_prp(self):          # Lines beginning with 'p'
        return
    def loadFile(self,sFileName):
        self.cameraFileName = sFileName

        with open(sFileName) as openCameraFile:
            print(' sFileName = ' + str(sFileName))
            for l in openObjectFile:
                l_parsed = l.split()
                l_type = l_parsed[0]
                l_parsed.pop(0)        


