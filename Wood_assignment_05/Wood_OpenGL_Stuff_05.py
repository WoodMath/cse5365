# Wood, Jeff
# 100-103-5461
# 2016-05-02
# Assignment_05

#   From
#       https://www.opengl.org/discussion_boards/showthread.php/136442-what-are-the-codes-for-arrow-keys-to-use-in-glut-keyboard-callback-function

import numpy as np
import copy
from numpy.linalg import inv
from numpy import linalg as LA

import OpenGL
from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *

iDelay = 30

class OpenGL_Stuff:
    def __init__(self, controller):
        self.controller = controller
        self.glList = 1
        self.displayState = True
        self.inputState = False
        self.width = None
        self.height = None
        self.eyeOffsetVector = None
        self.resetEyeOffset()
        self.filename = ''
        return

    def resetEyeOffset(self):
        self.eyeOffsetVector = [0,0,0]

    def createAxes(self):
        glNewList(2,GL_COMPILE)
        glBegin(GL_LINES)
        glColor3f(1,0,0)
        glVertex3f(0,0,0)
        glVertex3f(2,0,0)
        glEnd() 
                  
        glBegin(GL_LINES)
        glColor3f(0,1,0)
        glVertex3f(0,0,0)
        glVertex3f(0,2,0)
        glEnd() 
                  
        glBegin(GL_LINES)
        glColor3f(0,0,1)
        glVertex3f(0,0,0)
        glVertex3f(0,0,2)
        glEnd() 
        glEndList()
        
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
        if(self.displayState):
            for o in objs:
                self.createObject(o)

        glEndList()
                
        
    def display(self):
#        print(' Displaying stuff')
        self.displayCameras(self.controller.renderer.cameras)

        glFlush()
        glutSwapBuffers()
        ## glLoadIdentity()
#        print(' Finished Display')
        return

    
    def keyHandler(self, key, mouseX, mouseY):

#        print(' mouseX = ' + str(mouseX))
#        print(' mouseY = ' + str(mouseY))

#        if(self.inputState):
#            self.consoleInput(key)
#            return

        ## Load file
        if key == b'n' or key == b'N':
#            self.filename = input(' Input filname  : ')

            self.inputState = True
            self.displayState = False
            self.create()

#            print(' Input filname (Keep Focus on OpenGL window) : ', end='')

            print(' *** Change focus to Python Console *** ')
            result = input(' Load a file : ')
            self.filename = result
            print(' Loading \'' + str(result) + '\'')
            self.controller.addObjectFile(result)
            print(' *** Change focus back to OpenGL window *** ')
            self.inputState = False

        if key == b'd' or key == b'D':
            self.displayState = True
            self.create()

        if key == b'p' or key == b'P':
            for c in self.controller.renderer.cameras:
                c.toggleType()

        ## Rotate about x-Axis
        if key == b'x':
            glMatrixMode(GL_MODELVIEW)
            glRotated(5, 1, 0, 0)
        if key == b'X':
            glMatrixMode(GL_MODELVIEW)
            glRotated(-5, 1, 0, 0)

        ## Rotate about y-Axis
        if key == b'y':
            glMatrixMode(GL_MODELVIEW)
            glRotated(5, 0, 1, 0)
        if key == b'Y':
            glMatrixMode(GL_MODELVIEW)
            glRotated(-5, 0, 1, 0)

        ## Rotate about z-Axis
        if key == b'z':
            glMatrixMode(GL_MODELVIEW)
            glRotated(5, 0, 0, 1)
        if key == b'Z':
            glMatrixMode(GL_MODELVIEW)
            glRotated(-5, 0, 0, 1)

        ## Scale
        if key == b's':
            glMatrixMode(GL_MODELVIEW)
            glScalef(1.05, 1.05, 1.05)
        if key == b'S':
            glMatrixMode(GL_MODELVIEW)
            glScalef(1.00/1.05, 1.00/1.05, 1.00/1.05)

        ## Backward / Forward
        if key == b'b' or key == b'B':
            self.eyeOffsetVector[2] = 0.05/1.05
        if key == b'f' or key == b'F':
            self.eyeOffsetVector[2] = -0.05
    



        elif key == b'q' or key == b'Q':
            print ("Bye")
            sys.exit()
        elif key == b'\x1b':
            print ("Bye")
            sys.exit()

    def specialHandler(self, key, mouseX, mouseY):
        ## Left / Right
        if key == GLUT_KEY_LEFT:
            self.eyeOffsetVector[0] = 0.05
        if key == GLUT_KEY_RIGHT:
            self.eyeOffsetVector[0] = -0.05

        ## Up / Down
        if key == GLUT_KEY_DOWN:
            self.eyeOffsetVector[1] = -0.05
        if key == GLUT_KEY_UP:
            self.eyeOffsetVector[1] = 0.05

    
    def timer(self, dummy):
        self.display()
        glutTimerFunc(iDelay, self.timer,0)
        
    def reshape(self, width, height):
        self.width = width
        self.height = height

        print ("Width=", width, "Height=", height)


    def displayCameras(self, cams):

        for c in cams:
            self.displayCamera(c)

        ## Reset eyeOffsetVectorh
        self.resetEyeOffset()

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

        vecU = np.array(cam.vecU)
        vecV = np.array(cam.vecV)
        vecN = np.array(cam.vecN)
        dist = cam.distance
        eye = np.array(cam.eye)
        
        fUoffset = dist * self.eyeOffsetVector[0]
        fVoffset = dist * self.eyeOffsetVector[1]
        fNoffset = dist * self.eyeOffsetVector[2]

        vecU *= fUoffset
        vecV *= fVoffset
        vecN *= fNoffset      

        eye += (vecU+vecV+vecN)
        cam.addEye(eye)

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
#            cam.eye[0] + eyeOffset[0] , cam.eye[1] + eyeOffset[1], cam.eye[2] + eyeOffset[2],\
            cam.eye[0], cam.eye[1], cam.eye[2],\
            cam.lookAt[0], cam.lookAt[1], cam.lookAt[2],\
            cam.up[0], cam.up[1], cam.up[2]\
        )
        glMatrixMode(GL_MODELVIEW)    
        glViewport(screenLeft, screenBottom, screenWidth, screenHeight)

        glCallList(self.glList) 
        glPushMatrix()
        glLoadIdentity()
        glCallList(2) 
        glPopMatrix()
        return

    def create(self):
        self.controller.addCameraFile('cameras_05.txt')
#        print(' self.controller = ' + str(self.controller))
#        print(' self.controller.renderer = ' + str(self.controller.renderer))
#        print(' self.controller.renderer.scene = ' + str(self.controller.renderer.scene))
#        print(' self.controller.renderer.scene.objects = ' + str(self.controller.renderer.scene.objects))
        
        if(self.controller.renderer.scene.objects):
            self.createObjects(self.controller.renderer.scene.objects)
        else:
            print(' No object files have been sucessfully loaded !')
        self.createAxes()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def createWindow(self, width=800, height=600, left=100, top=100):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
        glutInitWindowSize(800, 500)
        glutInitWindowPosition(100, 100)
        self.width = width
        self.height = height
        self.controller.window = glutCreateWindow(b'Wood Assignment 05')
        glClearColor(1,1,0,0)
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS);
        
    def addCallbacks(self):
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyHandler)
        glutSpecialFunc(self.specialHandler)
        glutTimerFunc(300,self.timer,0)
        glutReshapeFunc(self.reshape)


    def mainLoop(self):
        glutMainLoop()

