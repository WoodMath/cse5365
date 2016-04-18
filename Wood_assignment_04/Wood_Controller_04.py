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

import time
fDelay = 0.1

class Controller:
    def __init__(self,root):
        self.root = root
        self.view = None
        self.world = None
        self.canvas = None
        self.panel = None
        self.renderer = self.addRenderer()

        self.fileName = None
        
        self.rotationAxisOptions = {'X':1,'Y':2,'Z':3,'LineAB':4}
        self.rotationAxisOption = None
        self.rotationAxisVectorA = None
        self.rotationAxisVectorB = None
        self.rotationAxis = None
        self.rotationDegrees = None
        self.rotationSteps = None
        
        self.scaleSizeOptions = {'Uniform':1,'NonUniform':2}
        self.scaleSizeOption = None
        self.scaleSizeScalar = None
        self.scaleSizeVector = None
        self.scaleCenterVector = None
        self.scaleSteps = None
        
        self.translationVector = None
        self.translationSteps = None

        self.flyVRPVectorA = None
        self.flyVRPVectorB = None
        self.flyVRPSteps = None
        
        self.cameraSelectedName = None
        self.cameraSelectedNumber = 0
        return
    def getCameraVRP_A(self):
        k = self.getCameraVRP_AB()
        return k['vrpA']
    def getCameraVRP_B(self):
        k = self.getCameraVRP_AB()
        return k['vrpB']
    def getCameraVRP_AB(self):
        c = self.renderer.cameras[self.cameraSelectedNumber]
        return {'vrpA':c.vrpA,'vrpB':c.vrpB}
    
    def setCameraVRP_A(self):
        c = self.renderer.cameras[self.cameraSelectedNumber]
        c.vrpA = self.flyVRPVectorA
    def setCameraVRP_B(self):
        c = self.renderer.cameras[self.cameraSelectedNumber]
        c.vrpB = self.flyVRPVectorB
    def setCameraVRP_AB(self):
        self.setCameraVRP_A()
        self.setCameraVRP_B()

    def updateVRPs(self):
        v_vrpA = self.getCameraVRP_A()
        v_vrpB = self.getCameraVRP_B()

        self.panel.vrp_ax.delete(0,"end")
        self.panel.vrp_ax.insert(0,'%.1f' % v_vrpA[0])
        self.panel.vrp_ay.delete(0,"end")
        self.panel.vrp_ay.insert(0,'%.1f' % v_vrpA[1])
        self.panel.vrp_az.delete(0,"end")
        self.panel.vrp_az.insert(0,'%.1f' % v_vrpA[2])

        self.panel.vrp_bx.delete(0,"end")
        self.panel.vrp_bx.insert(0,'%.1f' % v_vrpB[0])
        self.panel.vrp_by.delete(0,"end")
        self.panel.vrp_by.insert(0,'%.1f' % v_vrpB[1])
        self.panel.vrp_bz.delete(0,"end")
        self.panel.vrp_bz.insert(0,'%.1f' % v_vrpB[2])
        
    def loadObject(self):        
            
        self.renderer.addObjectFile(self.fileName)
        self.canvas.update()
        self.updateVRPs()
        return
    def addRenderer(self, renderer = Renderer()):
        self.renderer = renderer
        renderer.controller = self

        if(self.canvas != None):
            self.renderer.canvas = self.canvas
        renderer.addCameraFile('cameras_04.txt')
        return self.renderer
    def addView(self, view):
        self.view = view
        self.world = view.ob_world
        self.panel = view.panel
        self.canvas = view.ob_canvas_frame.canvas
        if(self.renderer != None):
            self.renderer.canvas = self.canvas
        view.controller = self
        view.ob_world.controller = self

        ## Now we have a view (widgets object) we can draw boxes
        if(self.renderer != None):
            self.renderer.createViewports()
            self.canvas.update()
            
    def setSize(self):
        iWidth = int(self.canvas.cget("width"))
        iHeight = int(self.canvas.cget("height"))

        self.renderer.setSize(iWidth, iHeight)

    def rotate(self):
        self.renderer.scene.establish_rotation_matrix()
        i_steps = (self.rotationSteps if self.rotationSteps > 1 else 1)
        
        for i_inc in range(i_steps):
            self.renderer.scene.applyMatrix(self.renderer.scene.rotationMatrix)
            self.renderer.updateCameras()
            self.canvas.update()
            if(i_steps>1):
                time.sleep(fDelay)
        
        return

    def scale(self):
        self.renderer.scene.establish_scale_matrix()
        i_steps = (self.scaleSteps if self.scaleSteps > 1 else 1)

        for i_inc in range(i_steps):
            self.renderer.scene.applyMatrix(self.renderer.scene.scaleMatrix)
            self.renderer.updateCameras()
            self.canvas.update()
            if(i_steps>1):
                time.sleep(fDelay)
                
        return

    def translate(self):
        self.renderer.scene.establish_translation_matrix()
        i_steps = (self.translationSteps if self.translationSteps > 1 else 1)

        for i_inc in range(i_steps):
            self.renderer.scene.applyMatrix(self.renderer.scene.translationMatrix)
            self.renderer.updateCameras()
            self.canvas.update()
            if(i_steps>1):
                time.sleep(fDelay)
                
        return

    def fly(self):
        i_cam = self.cameraSelectedNumber

        ## Reset VRP position, otherwise will perform offset of existing VRP position
        self.renderer.cameras[i_cam].setVRP(copy.copy(self.getCameraVRP_A()))
        
        self.renderer.cameras[i_cam].establish_fly_matrix()
        i_steps = (self.flyVRPSteps if self.flyVRPSteps > 1 else 1)

        for i_inc in range(i_steps):
            vTempVRP = self.renderer.cameras[i_cam].getVRP()
            print(' *** vTempVRP = ' + str(vTempVRP))
            mTempVRP = np.transpose(np.matrix([vTempVRP[0],vTempVRP[1],vTempVRP[2],1]))
            vTempVRP = np.array(np.transpose(self.renderer.cameras[i_cam].flyMatrix * mTempVRP))[0].tolist()
            print(' *** i_inc = ' + str(i_inc))
            self.renderer.cameras[i_cam].setVRP([vTempVRP[0],vTempVRP[1],vTempVRP[2]])
            print(' *** vTempVRP = ' + str(vTempVRP))
            self.renderer.cameras[i_cam].updateTransform()
            self.renderer.cameras[i_cam].updateCamera()
            self.canvas.update()
            
            if(i_steps>1):
                time.sleep(fDelay)
                
        return
    
    def update(self):
        self.renderer.updateScene()
        self.renderer.updateCameras()
        self.canvas.update()
        
    def resize(self):
        self.setSize()
        self.renderer.resizeViewports()
        self.renderer.resizeCameras()
        self.canvas.update()
        
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
        self.scaleSizeScalar = float(self.panel.sScaleSize.get())
        self.scaleSizeVector = [float(self.panel.sScaleSx.get()),float(self.panel.sScaleSy.get()),float(self.panel.sScaleSz.get())]
        self.scaleCenterVector = [float(self.panel.sScaleAx.get()),float(self.panel.sScaleAy.get()),float(self.panel.sScaleAz.get())]
        self.scaleSteps = int(self.panel.sScaleSteps.get())
        
        self.translationVector = [float(self.panel.sTransTx.get()),float(self.panel.sTransTy.get()),float(self.panel.sTransTz.get())]
        self.translationSteps = int(self.panel.sTransSteps.get())

        self.flyVRPVectorA = [float(self.panel.sVRPAx.get()), float(self.panel.sVRPAy.get()), float(self.panel.sVRPAz.get())]
        self.flyVRPVectorB = [float(self.panel.sVRPBx.get()), float(self.panel.sVRPBy.get()), float(self.panel.sVRPBz.get())]
        self.flyVRPSteps = int(self.panel.sFlySteps.get())        


        ## Save VRP Information to current camera.
        self.setCameraVRP_AB()
    
        ## Switch old viewport to normal
        c = self.renderer.cameras[self.cameraSelectedNumber]
        self.canvas.itemconfig(c.rectangle,width=1)

        ## Get new vieport selected
        self.cameraSelectedName = self.panel.camera.get()
        self.cameraSelectedNumber = self.panel.camera.current()

        print(' self.cameraSelectedNumber = ' + str(self.cameraSelectedNumber))
        ## Switch new viewport to 2x line width
        c = self.renderer.cameras[self.cameraSelectedNumber]
        self.canvas.itemconfig(c.rectangle,width=2)

        self.canvas.update()
        
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
