# Wood, Jeff
# 100-103-5461
# 2016-05-02
# Assignment_05
#
#   From
#       http://www.tutorialspoint.com/python/python_command_line_arguments.htm

import sys
import OpenGL

from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *

from Wood_Controller_05 import *

Angle = 0
Incr = 1

for k in sys.argv:
    print(str(k))

c = Controller()
c.addCameraFile('cameras_05.txt')
c.addObjectFile('cube_05.txt')
c.addObjectFile('pyramid_05.txt')
c.go()
