# Wood, Jeff
# 100-103-5461
# 2016-05-02
# Assignment_05

#   From
#       http:

import sys
import OpenGL

from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *


class OpenGL_Stuff():
    def __init__(self, controller):
        self.controller = controller
        return
    def createObject(self,obj):
        # 3 for triangles
        # 4 for quads
        # 5 for other
        print(obj.get())

        glBegin(GL_TRIANGLES)
        iPrevState = 3
        for f in obj.faces:
            iCurrState = len(f) if len(f) < 5 else 5
            if(iCurrState != iPrevState or iPrevState == 5):
                ## Need to restart polygon regardless
                glEnd()
                if(iCurrState == 3):
                    glBegin(GL_TRIANGLES)
                if(iCurrState == 4):
                    glBegin(GL_QUADS)
                if(iCurrState == 5):
                    glBegin(GL_POLYGONS)
            iPrevState = iCurrState
            for i in f:
                v = obj.vertices[i]
                glVertex3f(v[0], v[1], v[2])
            
        glEnd()
    def createObjects(self,objs):
        glNewList(1,GL_COMPILE)
        for o in objs:
            self.createObject(o)
        glEndList()
    def createWindow(self, width=800, height=600, left=100, top=100):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
        glutInitWindowSize(800, 500)
        glutInitWindowPosition(100, 100)
        self.controller.window = glutCreateWindow(b"PyOpenGL Demo")
        glClearColor(1,1,0,0)
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS);
        
    def addCallbacks(self):
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyHandler)
        glutTimerFunc(300,self.timer,0)
        glutReshapeFunc(self.reshape)
        
        
    def display(self):
        print(' Displaying stuff')
        return


    def keyHandler(self, Key, MouseX, MouseY):
        global Incr
        if Key == b'f' or Key == b'F':
            print (b"Speeding Up")
            Incr = Incr + 1
        elif Key == b's' or Key == b'S':
            if Incr == 0:
                print ("Stopped")
            else:
                print ("Slowing Down")
                Incr = Incr - 1
        elif Key == b'q' or Key == b'Q':
            print ("Bye")
            sys.exit()
        else:
            print ("Invalid Key ",Key)
    
    def timer(self, dummy):
        self.display()
        glutTimerFunc(30, self.timer,0)
        
    def reshape(self, width, height):
        self.controller.renderer.width = width
        self.controller.renderer.height = height

        print ("Width=", width, "Height=", height)


    def mainLoop(self):
        glutMainLoop()
