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
        self.cameraFileName = []

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

        return

    def get(self):
        return {'scenes':self.scenes, \
                'cameraFileName':self.cameraFileName, \
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

    def addScene(self, scn):
        self.scenes.append(scn)
        
    def clearScenes(self):
        self.scenes = []
    def addInfo(self, sInfo):                  # Lines beginning with 'i'
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
        return
    def addViewport(self, lViewport):           # Lines beginning wtih 's'
        self.viewport = lViewport
        self.vx = [lViewport[0], lViewport[1]]
        self.vy = [lViewport[2], lViewport[3]]
        return
    def addVRP(self, vVRP):                     # Lines beginning with 'r'
        self.vrp = vVRP
        return
    def addVPN(self, vVPN):                     # Lines beginning with 'n'
        self.vpn = vVPN
        return
    def addVUP(self, vVUP):                     # Lines beginning with 'u'
        self.vup = vVUP
        return
    def addPRP(self, vPRP):                     # Lines beginning with 'p'
        self.prp = vPRP
        return
       


