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

from Wood_Renderer_05 import *

Angle = 0
Incr = 1
        

r = Renderer()
r.addCameraFile('cameras_05.txt')
