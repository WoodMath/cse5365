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
        self.objectFileName = None
        self.faceIndices = []
        self.lineIndices = []
        self.facePoints = []
        self.linePoints = []

        ## Variables containing optimal placement
        self.start_index = []                   # Array keeping track of each starting position in lineIndices
        self.group_count = []                   # Array keeping track of each group size in lineIndecies
        
        return
    def get(self):
        return {'objectFileName': self.objectFileName, \
                'faceIndices': self.faceIndices, \
                'lineIndices': self.lineIndices, \
                'facePoints': self.facePoints, \
                'linePoints': self.linePoints}

    def addPoint(self, l_parsed):
        self.facePoints.append(l_parsed)        ## Append to faces
        self.linePoints.append(l_parsed)        ## Append to lines
    def addIndice(self, l_parsed):
        ## Faces can have any number of indices
        self.faceIndices.append(l_parsed)       

        ## Lines should only have two indices
        for k in range(len(l_parsed)-1):
            l_passed = [l_parsed[k],l_parsed[k+1]]

            if(l_passed[0] < l_passed[1]):
                self.position( [l_passed[0], l_passed[1]], self.lineIndices)
                                
            if(l_passed[1] < l_passed[0]):
                self.position( [l_passed[1], l_passed[0]], self.lineIndices)
                            
        ## Add line back to beginning, since some formats do not repeat first vertex for closed shape
        if(len(l_parsed)>2):
            if(l_parsed[0] != l_parsed[len(l_parsed)-1]):      
                l_passed = [l_parsed[0], l_parsed[len(l_parsed)-1]]

                if(l_passed[0] < l_passed[1]):
                    self.position( [l_passed[0], l_passed[1]], self.lineIndices)
                                
                if(l_passed[1] < l_passed[0]):
                    self.position( [l_passed[1], l_passed[0]], self.lineIndices)


    def position(self, v_to_add, arr_add_to):
        ## Performs a prefix sort / radix sort
        ## Cycles through an array of 2 element arrays such to insert an array [x,y] such that
        ##      All elements x are no less than the elements x before it.
        ##      For any given x, all elements y are no less than the elements y before it
        ##      Think [[0,0,1],[0,1,1],[0,2,1],[1,0,1],[1,1,1],[1,2,1],[2,0,1],[2,1,1],[2,2,1]]
#        print('v_to_add = ' + str(v_to_add))
        i_current_vert_group = v_to_add[0]
        i_current_vert_group_count = len(self.start_index)
        
        if(i_current_vert_group < i_current_vert_group_count):
            if(self.start_index[i_current_vert_group] == -1):
                ## First edge in group (with v_to_add[0])
                i_found = -1
                i_previous_group = -1
                for i_inc in range(0,i_current_vert_group):
                    if(self.start_index[i_inc] > -1):
                        i_previous_group = i_inc;
                        i_found = i_inc;

                if(i_found == -1):                                      ## No previous start found
                    i_start = 0                                         ## Just use 0
                else:                                                   ## Otherwise
                    i_start = \
                            self.start_index[i_previous_group] + self.group_count[i_previous_group]
                    ## Use start of Previous group start Plus previous group size

                self.start_index[i_current_vert_group] = i_start        ## Set group start for first time

                ## Inser occurs at group start
                i_ins = self.start_index[i_current_vert_group]
                
            else:
                ## Get elements to cycle throug
                i_index_start = self.start_index[i_current_vert_group]
                i_index_stop = i_index_start + self.group_count[i_current_vert_group]

                i_found = -1
                i_inc = i_index_start
                for i_inc in range(i_index_start, i_index_stop):
                    v_test = arr_add_to[i_inc]
                    if(v_test[0] != i_current_vert_group):  ## Something happended causing to go outside the current group
                        ValueError(' Something bad happened: v_test[0] = ' + str(v_test[0]) + \
                                   ' Not the same as i_current_vert_group = ' + str(i_current_vert_group))
                    if(v_test[1] == v_to_add[1]):           ## Dubplicate is being inserted
                        i_ins = -1                          ## Do not insert
                        i_found = i_inc                     ## Place found
                        break
                    if(v_test[1] > v_to_add[1]):
                        i_ins = i_inc                       ## Insert occurs at place it fails
                        i_found = i_inc                     ## Place found
                        break
                    
                if(i_found == -1):                          ## No insert place found    
                    i_ins = i_inc + 1                       ## Choose next spot
                    i_found = i_ins
            
        else:
            ## Keep adding dummy elemends
            for i_inc in range(i_current_vert_group_count,i_current_vert_group):
                self.start_index.append(-1)                 ## To start indice array
                self.group_count.append(0)                  ## And group size array
            i_ins = len(arr_add_to)                         ## Set insert position as end of vertice list
            self.start_index.append(i_ins)                  ## Set the start to this position
            self.group_count.append(0)                      ## Still keeping group size as 0 because element hasn't been appendied to vertice list yet

        ## Found position to insert
        i_current_vert_group_count = len(self.start_index)  ## Restablish group count

        ## Now do insert
        if(i_ins > -1):
            arr_add_to.insert(i_ins,v_to_add)               ## Insert actual vertex
            (self.group_count[i_current_vert_group]) += 1   ## Increase the group size by 1

            for i_inc in range(i_current_vert_group+1, i_current_vert_group_count):
                (self.start_index[i_inc]) += 1              ## Increment starting index of remaining group

    def loadFile(self,sFileName):
        self.objectFileName = sFileName

        with open(sFileName) as openObjectFile:
            print(' sFileName = ' + str(sFileName))
            for l in openObjectFile:
                l_parsed = l.split()
                l_type = l_parsed[0]
                l_parsed.pop(0)
                    
                if(len(l_parsed)>0):
                    if(l_type == 'v'):
                        l_parsed.append('1.0')
                        l_parsed = vect_float(l_parsed)
                        self.addPoint(l_parsed)                        
                    elif(l_type == 'f'):
                        l_parsed.append('1')
                        l_parsed = vect_int_less_one(l_parsed)
                        self.addIndice(l_parsed)                        
                    else:
                        raise ValueError(' "' + str(l_type) + '" Not valid ')
        self.seperatePoints()   ## Make sure each point is only referenced by 1 line

    def seperatePoints(self):
        ## Makes sure each point is only referrred to 1 (at most line)
        ## i.e. multiple indices do not reference the same point.
        v_points = copy.copy(self.linePoints)
        v_indices = copy.copy(self.lineIndices)
        v_out_points=[]
        v_out_indices=[]
        i_index = 0
        for i_inc in range(0,len(v_indices)):
            i_index_one = v_indices[i_inc][0]
            i_index_two = v_indices[i_inc][1]
            v_point_one = v_points[i_index_one]
            v_point_two = v_points[i_index_two]
            
            v_out_points.append(v_point_one)
            v_out_points.append(v_point_two)

            v_out_indices.append([i_index,i_index+1,1])
            i_index += 2

        self.linePoints = v_out_points
        self.lineIndices = v_out_indices



#k=Object()
#k.loadFile('C:/Users/Jeff/Dropbox/cse5365/assignments/Wood_assignment_04/pyramid_04.txt')

#print(' k.facePoints = ')
#print(k.facePoints)
#print(' k.faceIndices = ')
#print(k.faceIndices)
#print(' k.linePoints = ')
#print(k.linePoints)
#print(' k.lineIndices = ')
#print(k.lineIndices)


