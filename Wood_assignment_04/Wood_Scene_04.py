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

from Wood_Object_04 import *

class Scene():
    def __init__(self):

        self.objects = []
        self.points = []
        self.indices = []

        return

    def get(self):
        return {'objects':[o.get() for o in self.objects ],'points':self.points,'indices':self.indices}

    def addObject(self, obj):
        ## Append objects
        self.objects.append(obj)

        ## Establis current point index
        i_point_index = len(self.points)

        ## Append object points and indices
        for i in range(len(obj.lineIndices)):
            i_ind0 = obj.lineIndices[i][0]
            i_ind1 = obj.lineIndices[i][1]
            p0 = obj.linePoints[i_ind0]
            p1 = obj.linePoints[i_ind1]

            self.points.append(p0)
            self.points.append(p1)
            self.indices.append([i_ind0 + i_point_index, i_ind1 + i_point_index, 1])
        
    def clearObjects(self):
        self.objects = []
        self.points = []
        self.indices = []
        



