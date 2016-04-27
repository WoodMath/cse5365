# Wood, Jeff
# 100-103-5461
# 2016-05-02
# Assignment_05

#   From
#       http:

import numpy as np
import copy
from numpy.linalg import inv
from numpy import linalg as LA

import sys

import OpenGL
from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *


class OpenGL_Stuff():
    def __init__(self, controller):
        self.controller = controller
        self.glList = 1
        self.width = None
        self.height = None
        return
    def createObject(self,obj):
        # 3 for triangles
        # 4 for quads
        # 5 for other
#        print(obj.get())

        glBegin(GL_TRIANGLES)
#        print(' glBegin(GL_TRIANGLES) ')
        iPrevState = 3
        for f in obj.faces:
            iCurrState = len(f) if len(f) < 5 else 5
#            print(' %% iCurrState = ' + str(iCurrState) + ' ; iPrevState = ' + str(iPrevState))
            if(iCurrState != iPrevState or iPrevState == 5):
                ## Need to restart polygon regardless
                glEnd()
#                print(' glEnd() ')
                if(iCurrState == 3):
                    glBegin(GL_TRIANGLES)
#                    print(' glBegin(GL_TRIANGLES) ')
                if(iCurrState == 4):
                    glBegin(GL_QUADS)
#                    print(' glBegin(GL_QUADS) ')
                if(iCurrState == 5):
                    glBegin(GL_POLYGONS)
#                    print(' glBegin(GL_POLYGONS) ')
            iPrevState = iCurrState
#            print(' %% iCurrState = ' + str(iCurrState) + ' ; iPrevState = ' + str(iPrevState))

            v0 = np.array(obj.vertices[f[0]])
            v1 = np.array(obj.vertices[f[1]])
            v2 = np.array(obj.vertices[f[2]])

            vecA = v0 - v1
            vecB = v2 - v1

            vecP = np.cross(vecA,vecB)
            vecP = vecP/LA.norm(vecP)
            vecP1 = (vecP + np.array([1.0, 1.0, 1.0]))*0.25 + np.array([0.5, 0.5, 0.5])
            fColorR = copy.copy(vecP1[0])
            fColorG = copy.copy(vecP1[1])
            fColorB = copy.copy(vecP1[2])

            glColor3f(fColorR, fColorG, fColorB)
            
            for i in f:
                v = obj.vertices[i]
                glVertex3f(v[0], v[1], v[2])
#                print(' glVertex3f(' + str(v[0]) + ',' + str(v[1]) + ',' + str(v[2]) + ') ')
            
        glEnd()
#        print(' glEnd() ')
    def createObjects(self,objs):


        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)

        glNewList(self.glList,GL_COMPILE)
        for o in objs:
            self.createObject(o)
        glEndList()
    def createWindow(self, width=800, height=600, left=100, top=100):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
        glutInitWindowSize(800, 500)
        glutInitWindowPosition(100, 100)
        self.width = width
        self.height = height
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
        self.displayCameras(self.controller.renderer.cameras)

        glFlush()
        glutSwapBuffers()
        ## glLoadIdentity()
        print(' Finished Display')
        return


    def keyHandler(self, key, mouseX, mouseY):
        global incr

        print(' key = ' + str(key))
        print(' mouseX = ' + str(mouseX))
        print(' mouseY = ' + str(mouseY))

        if key == b'n' or key == b'N':
            result = input(' Load a file : ')
            print(' result = ' + str(result))

        if key == b'd' or key == b'D':
            result = input(' Load a file : ')
            print(' result = ' + str(result))

        elif key == b'f' or key == b'F':
            print (b"Speeding Up")
            incr = incr + 1
        elif key == b's' or key == b'S':
            glMatrixMode(GL_MODELVIEW)
            glScalef(2.0, 2.0, 2.0)

        elif key == b'q' or key == b'Q':
            print ("Bye")
            sys.exit()
        elif key == b'\x1b':
            print ("Bye")
            sys.exit()
        else:
            print ("Invalid Key ", key)
    
    def timer(self, dummy):
        self.display()
        glutTimerFunc(30, self.timer,0)
        
    def reshape(self, width, height):
        self.width = width
        self.height = height

        print ("Width=", width, "Height=", height)


    def displayCameras(self, cams):

        for c in cams:
            self.displayCamera(c)

    def displayCamera(self, cam):
        viewportWidth = cam.vx[1] - cam.vx[0]
        viewportHeight = cam.vy[1] - cam.vy[0]
        viewportLeft = cam.vx[0]
        viewportBottom = cam.vy[0]

        screenWidth = int(viewportWidth * self.width)
        screenHeight = int(viewportHeight * self.height)
        screenLeft = int(viewportLeft * self.width)
        screenBottom = int(viewportBottom * self.height)

#        print(' *** ')
#        print(' screenWidth = ' + str(screenWidth) + ' ; type(screenWidth) = ' + str(type(screenWidth)))
#        print(' screenHeight = ' + str(screenHeight) + ' ; type(screenHeight) = ' + str(type(screenHeight)))
#        print(' screenLeft = ' + str(screenLeft) + ' ; type(screenLeft) = ' + str(type(screenLeft)))
#        print(' screenBottom = ' + str(screenBottom) + ' ; type(screenBottom) = ' + str(type(screenBottom)))

        ## From code provided by instructor
        glEnable(GL_SCISSOR_TEST)
        glScissor(screenLeft, screenBottom, screenWidth, screenHeight)
        glClearColor(0.4,0.4,0.6,0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if(cam.type == 'parallel'):
            glOrtho(cam.wu[0], cam.wu[1], cam.wv[0], cam.wv[1], cam.wn[0], cam.wn[1])
        if(cam.type == 'perspective'):
            glFrustum(cam.wu[0], cam.wu[1], cam.wv[0], cam.wv[1], cam.wn[0], cam.wn[1])
#        gluLookAt(0,0,3,0,0,0,0,1,0)
        gluLookAt(\
            cam.eye[0], cam.eye[1], cam.eye[2],\
            cam.lookAt[0], cam.lookAt[1], cam.lookAt[2],\
            cam.up[0], cam.up[1], cam.up[2]\
        )
        glMatrixMode(GL_MODELVIEW)    
        glViewport(screenLeft, screenBottom, screenWidth, screenHeight)

        glCallList(self.glList) 
        glPushMatrix()
#        glLoadIdentity()
#        glCallList(2) 
        glPopMatrix()
        return

    def mainLoop(self):
        glutMainLoop()

