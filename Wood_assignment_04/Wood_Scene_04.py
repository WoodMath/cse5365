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
from wood_transform_03 import *
from wood_clipping_03 import *

from Wood_Object_04 import *

class Scene():
    def __init__(self):

        self.objects = []

        return

    def addObject(self, obj):
        self.objects.append(obj)
        
    def clearObjects(self, obj):
        self.objects.append(obj)
        




s = Scene()
