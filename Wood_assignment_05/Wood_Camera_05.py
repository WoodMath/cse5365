# Wood, Jeff
# 100-103-5461
# 2016-05-02
# Assignment_05
#
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

import time
fDelay = 0.5

class Camera:
    def __init__(self,renderer):
        print(' ************************** ')
        self.scene = None

        ## tags from 'camera' file
        self.info = None
        self.type = None
        self.eye = None
        self.lookAt = None
        self.up = None
        self.window = None
        self.viewport = None

        ## tags below derived from 'self.window' and 'self.viewport' defined above
        self.wu = None
        self.wv = None
        self.wn = None
        self.vx = None
        self.vy = None

        self.rectangle = None
        self.text = None

        ## Added
        self.x01 = None
        self.y01 = None



    def get(self):
        return {'info':self.info, \
                'type':self.type, \
                'eye':self.eye, \
                'lookAt':self.lookAt, \
                'up':self.up, \
                'window':self.window, \
                'viewport':self.viewport, \
                'wU':self.wu, \
                'wV':self.wv, \
                'wN':self.wn, \
                'vX':self.vx, \
                'vY':self.vy}

        
    def addInfo(self, sInfo):                   # Lines beginning with 'i'
        self.info = sInfo[0]
        return
    def addType(self, sType):                   # Lines beginning with 't'
        self.type = sType[0]
        return
    def addWindow(self, lWindow):               # Lines beginning with 'w'
        self.window = lWindow
        self.wu = [lWindow[0], lWindow[1]]
        self.wv = [lWindow[2], lWindow[3]]
        self.wn = [lWindow[4], lWindow[5]]
        return
    def addViewport(self, lViewport):           # Lines beginning wtih 's'
        self.viewport = lViewport
        self.vx = [lViewport[0], lViewport[2]]
        self.vy = [lViewport[1], lViewport[3]]
        return
    def addEye(self,vEye):
        self.eye = vEye
    def addLookAt(self, vLookAt):                     # Lines beginning with 'r'
        self.lookAt = vLookAt
        return
    def addUp(self, vUp):                     # Lines beginning with 'n'
        self.up = vUp
