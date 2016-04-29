# Wood, Jeff
# 100-103-5461
# 2016-05-02
# Assignment_05
#
#   From
#       http://www.jesshamrick.com/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/
#       http://stackoverflow.com/questions/1607612/python-how-do-i-make-a-subclass-from-a-superclass
#       http://jfine-python-classes.readthedocs.org/en/latest/subclass-int.html
#       https://docs.python.org/3.5/tutorial/classes.html
#       https://docs.python.org/2/tutorial/classes.html
#       http://learnpythonthehardway.org/book/ex44.html

import sys

import numpy as np
import copy
from numpy.linalg import inv
from numpy import linalg as LA

def single_int(passed_int):
    return int(passed_int)
def single_int_less_one(passed_int):
    return int(passed_int)-1
def single_float(passed_float):
    return float(passed_float)

#vect_int=np.vectorize(int)
#vect_int_less_one=np.vectorize(single_int_less_one)
#vect_float=np.vectorize(float)

def vect_int(passed_arr):
    v_rtrn = []
    for i in range(len(passed_arr)):
        v_rtrn.append(int(passed_arr[i]))
    return v_rtrn

def vect_int_less_one(passed_arr):
    v_rtrn = []
    for i in range(len(passed_arr)):
        v_rtrn.append(int(passed_arr[i])-1)
    return v_rtrn
    
def vect_float(passed_arr):
    v_rtrn = []
    for i in range(len(passed_arr)):
        v_rtrn.append(float(passed_arr[i]))
    return v_rtrn


class Object:
    def __init__(self):
        self.clear()
    def clear(self):
        self.objectFileName = None
        self.vertices = []
        self.faces = []
        
        
        return
    def get(self):
        return {'objectFileName': self.objectFileName, \
                'vertices': self.vertices, \
                'faces': self.faces }

    def addVertice(self, l_parsed):
        self.vertices.append(l_parsed)

    def addFace(self, l_parsed):
        self.faces.append(l_parsed)

        ## Lines should only have two indices

    def loadFile(self,sFileName):
#        print(' ' + str(self.__class__.__name__) + '.' + str(sys._getframe().f_back.f_code.co_name) + '() called')
        
        self.objectFileName = sFileName

        with open(sFileName) as openObjectFile:
            
            for l in openObjectFile:
                l_parsed = l.split()
                l_type = l_parsed[0]
                l_parsed.pop(0)
                if(len(l_parsed)>0):
                    if(l_type == 'v'):
                        l_parsed = vect_float(l_parsed)
                        self.addVertice(l_parsed)                        
                    elif(l_type == 'f'):
                        l_parsed = vect_int_less_one(l_parsed)
                        self.addFace(l_parsed)                        
                    else:
                        print(' "' + str(l) + '" Not valid ')
                        raise ValueError(' "' + str(l) + '" Not valid ')

