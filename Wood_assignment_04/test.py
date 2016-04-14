import numpy as np

from Wood_Object_04_test import *


o = Object()
#o1.loadFile('C:/Users/Jeff/Dropbox/cse5365/assignments/Wood_assignment_04/cube_04.txt')
o.loadFile('teapot_04.txt')
#print(' o.get() = ' + str(o.get()))

#o.addIndice([1,9,10,2])
#o.addIndice([2,10,11,3])
#o.addIndice([3,11,12,4])

print(' len(o.lineIndices) = ' + str(len(o.lineIndices)))
