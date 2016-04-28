# Wood, Jeff
# 100-103-5461
# 2016-05-02
# Assignment_05
#
#   From
#       http://www.jesshamrick.com/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/

from Wood_Renderer_05 import *
from Wood_OpenGL_Stuff_05 import *

class Controller:
    def __init__(self):
        self.renderer = Renderer(self)
        self.opengl = OpenGL_Stuff(self)
        self.window = None
        return
    def addCameraFile(self, sFileName):
        self.renderer.addCameraFile(sFileName)
    def addObjectFile(self, sFileName):
        self.renderer.addObjectFile(sFileName)
    def createWindow(self, width=800, height=600, left=100, top=100):
        self.opengl.createWindow(width, height, left, top)
    def addCallbacks(self):
        self.opengl.addCallbacks()
    def mainLoop(self):
        self.opengl.mainLoop()
    
    def go(self):
        self.createWindow(400,300)
        self.addCallbacks()
        self.opengl.createObjects(self.renderer.scene.objects)
        self.opengl.createAxes()
#        self.opengl.drawCameras(self.renderer.cameras)

        self.mainLoop()
        
