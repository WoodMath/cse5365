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

'''
    ***************************************************
    **  See README.txt for instructions on running.  **
    ***************************************************
'''


c = Controller()


c.addObjectFile('pyramid_05.txt')
for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    print(' arg = ' + str(arg))
    c.addObjectFile(arg)

c.go()

