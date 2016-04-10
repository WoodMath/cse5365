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

from Wood_Renderer_04 import *
from Wood_Scene_04 import *

class Controller:
    def __init__(self):
        self.addRenderer()
        self.view = None
        self.world = None
        self.canvas = None
        self.panel = None

        self.fileName = None
        self.rotationAxisOptions = {'X':1,'Y':2,'Z':3,'LineAB':4}
        self.rotationAxis = None
        self.rotationDegrees = None
        self.rotationSteps = None
        self.scaleSizeOptions = {'Uniform':1,'NonUniform':2}
        self.scaleSizeVector = None
        self.scaleCenterVector = None
        self.scaleSteps = None
        self.translationVector = None
        self.cameraSelectedName = None
        self.cameraSelectedNumber = None
        return
    def addRenderer(self, renderer = Renderer()):
        self.renderer = renderer
        renderer.controller = self
        renderer.addCameraFile('cameras_04.txt')
    def addView(self, view):
        self.view = view
        self.world = view.ob_world
        self.panel = view.panel
        self.canvas = view.ob_canvas_frame.canvas
        view.controller = self
        view.ob_world.controller = self

        ## Now we have a view (widgets object) we can draw boxes
        if(self.renderer != None):
            self.renderer.createViewports()
    def setSize(self):
        iWidth = int(self.canvas.cget("width"))
        iHeight = int(self.canvas.cget("height"))

        self.renderer.setSize(iWidth, iHeight)
        
    def updateView(self):
        return
    def saveFormValues(self):
        
        self.fileName = self.panel.filename.get()
        self.rotationAxisOptions = {'X':1,'Y':2,'Z':3,'LineAB':4}
        self.rotationAxisOption = self.panel.i_rotate_option.get()
        self.rotationAxisVectorA = [float(self.panel.sRotateAx.get()),float(self.panel.sRotateAy.get()),float(self.panel.sRotateAz.get())]
        self.rotationAxisVectorB = [float(self.panel.sRotateBx.get()),float(self.panel.sRotateBy.get()),float(self.panel.sRotateBz.get())]
        self.rotationDegrees = int(self.panel.sRotateDegrees.get())
        self.rotationSteps = int(self.panel.sRotateSteps.get())   
        self.scaleSizeOptions = {'Uniform':1,'NonUniform':2}
        self.scaleSizeOption = self.panel.i_scale_option.get()
        self.scaleSizeVector = [float(self.panel.sScaleSx.get()),float(self.panel.sScaleSy.get()),float(self.panel.sScaleSz.get())]
        self.scaleCenterVector = [float(self.panel.sScaleAx.get()),float(self.panel.sScaleAy.get()),float(self.panel.sScaleAz.get())]
        self.scaleSteps = int(self.panel.sScaleSteps.get())
        self.translationVector = [float(self.panel.sTransTx.get()),float(self.panel.sTransTy.get()),float(self.panel.sTransTz.get())]
        self.translationSteps = int(self.panel.sTransSteps.get())

        self.cameraSelectedName = self.panel.camera.get()
        self.cameraSelectedNumber = self.panel.camera.current()

        
        
        return

    def get(self):
        return {'fileName':self.fileName,\
                'rotationAxisOptions':self.rotationAxisOptions,\
                'rotationAxisOption':self.rotationAxisOption,\
                'rotationAxisVectorA':self.rotationAxisVectorA,\
                'rotationAxisVectorB':self.rotationAxisVectorB,\
                'rotationDegrees':self.rotationDegrees,\
                'rotationSteps':self.rotationSteps,\
                'scaleSizeOptions':self.scaleSizeOptions,\
                'scaleSizeOption':self.scaleSizeOption,\
                'scaleSizeVector':self.scaleSizeVector,\
                'scaleCenterVector':self.scaleCenterVector,\
                'scaleSteps':self.scaleSteps,\
                'translationVector':self.translationVector,\
                'translationSteps':self.translationSteps,\
                'cameraSelectedName':self.cameraSelectedName,\
                'cameraSelectedNumber':self.cameraSelectedNumber}
