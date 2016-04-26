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

Angle = 0
Incr = 1
        
def create_pyramid():
      glNewList(1,GL_COMPILE)
      glBegin(GL_TRIANGLES)

      glVertex3f(0,0,0)
      glVertex3f(1,1,0)
      glVertex3f(0,1,0)
      glVertex3f(0,0,0)
      glVertex3f(1,0,0)
      glVertex3f(1,1,0)
      
      glColor3f(0,1,0)
      glVertex3f(0,0,0)
      glVertex3f(0,1,0)
      glVertex3f(0.5,0.5,1)
      
      glColor3f(0,0,1)
      glVertex3f(0,1,0)
      glVertex3f(1,1,0)
      glVertex3f(0.5,0.5,1)
      
      glColor3f(1,1,0)
      glVertex3f(1,1,0)
      glVertex3f(1,0,0)
      glVertex3f(0.5,0.5,1)
      
      glColor3f(1,0,1)
      glVertex3f(1,0,0)
      glVertex3f(0,0,0)
      glVertex3f(0.5,0.5,1)
      
      
      glEnd() 
      glEndList()

def create_3d_axes():
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

def display():
      global Angle
      global Incr
      w=glutGet(GLUT_WINDOW_WIDTH)
      h=glutGet(GLUT_WINDOW_HEIGHT)
      
      ## Upper-Left
      glEnable(GL_SCISSOR_TEST)
      glScissor(int(0.05*w),int(0.55*h),int(0.4*w),int(0.4*h))
      glClearColor(0.4,0.4,0.6,0)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      glFrustum(-1,1,-1,1,1,30)
      gluLookAt(0,0,3,0,0,0,0,1,0)
      glMatrixMode(GL_MODELVIEW)    
      glViewport(int(0.05*w),int(0.55*h),int(0.4*w),int(0.4*h))
      glCallList(1) 
      glPushMatrix()
      glLoadIdentity()
      glCallList(2) 
      glPopMatrix()
      
      ## Lower-Left
      glEnable(GL_SCISSOR_TEST)
      glScissor(int(0.05*w),int(0.05*h),int(0.4*w),int(0.4*h))
      glClearColor(0.4,0.4,0.6,0)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      glFrustum(-1,1,-1,1,1,30)
      gluLookAt(0,3,0,0,0,0,0,0,1)
      glMatrixMode(GL_MODELVIEW)      
      glViewport(int(0.05*w),int(0.05*h),int(0.4*w),int(0.4*h))
      glCallList(1)
      glPushMatrix()
      glLoadIdentity()
      glCallList(2) 
      glPopMatrix()      
      
      ## Upper-Right
      glScissor(int(0.55*w),int(0.55*h),int(0.4*w),int(0.4*h))
      glClearColor(0.4,0.4,0.6,0)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      #glFrustum(-1,1,-1,1,1,30)
      gluPerspective(45,.5,1,30)
      gluLookAt(3,0,0,0,0,0,0,1,0)
      glMatrixMode(GL_MODELVIEW)         
      glViewport(int(0.55*w),int(0.55*h),int(0.4*w),int(0.4*h))
      glCallList(1)  
      glPushMatrix()
      glLoadIdentity()
      glCallList(2) 
      glPopMatrix() 
      
      ## Lower-Right
      glScissor(int(0.55*w),int(0.05*h),int(0.4*w),int(0.4*h))
      glClearColor(0.4,0.4,0.6,0)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      glOrtho(-1,1,-1,1,1,30)
      #glFrustum(-1,1,-1,1,1,30)
      gluLookAt(2,2,2,0,0,0,0,1,0)
      glMatrixMode(GL_MODELVIEW)      
      glViewport(int(0.55*w),int(0.05*h),int(0.4*w),int(0.4*h))
      glCallList(1)
      glPushMatrix()
      glLoadIdentity()
      glCallList(2) 
      glPopMatrix()      
      
      glFlush()
      glutSwapBuffers()                 
      
      glLoadIdentity()
      glRotated(Angle,0,1,0)
      Angle = Angle + Incr


def keyHandler(Key, MouseX, MouseY):
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

def timer(dummy):
      display()
      glutTimerFunc(30,timer,0)
def reshape(w, h):
      print ("Width=",w,"Height=",h)

def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
    glutInitWindowSize(800, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"PyOpenGL Demo")
    glClearColor(1,1,0,0)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS);

def callbacks():
    glutDisplayFunc(display)
    glutKeyboardFunc(keyHandler)
    glutTimerFunc(300,timer,0)
    glutReshapeFunc(reshape)

def draw():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    create_pyramid()
    create_3d_axes()

def main():
    init()
    callbacks()
#    draw()
    glutMainLoop()

main()

