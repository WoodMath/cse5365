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

        self.clearObjects()

        return
    
    def clearObjects(self):
        self.objects = []
        self.points = []
        self.indices = []
        self.stack = np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        self.eye = np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        self.rotationMatrix = np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        self.scaleMatrix = np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        self.translationMatrix = np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        
    def updateScene(self):
        print(' Updating scene ...')
        self.world = np.transpose(self.stack * np.transpose(np.matrix(self.points))).tolist()
        return
    def get(self):
        return {'objects':[o.get() for o in self.objects ],'points':self.points,'indices':self.indices}

    def addObject(self, obj):
        ## Append objects
        self.objects.append(obj)

        ## Establish current point index
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

    def applyMatrix(self, mMatrix):
        
        self.stack = np.matrix(mMatrix) * self.stack
        self.world = np.transpose(self.stack * np.transpose(np.matrix(self.points)))
        
    def establish_rotation_matrix(self, i_steps, v_a, v_b, i_degree):
        # Establish the rotation matrix
        
        print(' Establishing rotation matrix ')
        v_a = np.array(v_a)
        v_b = np.array(v_b)
        v_ab = v_b-v_a
        
        f_x = v_ab[0]
        f_y = v_ab[1]
        f_z = v_ab[2]
        v_xyz = np.array([f_x,f_y,f_z,1])
        m_xyz = np.transpose(np.matrix(v_xyz))

        f_degree = float(i_degree)
        f_steps = float(i_steps)
        f_degree = f_degree / f_steps

        ###############################

        ## Establish matrix for translating all points
        ## such that vector 'a' lies at origin
        m_Rotate_Trans = np.matrix(\
            [[1,0,0,-v_a[0]],\
             [0,1,0,-v_a[1]],\
             [0,0,1,-v_a[2]],\
             [0,0,0,1]])
        ## establish inverse matrix (to save time vs. 'np.inverse(m_Rotate_Trans)')
        ## to translate points back again at end of process
        m_Rotate_Trans_Inv = np.matrix(\
            [[1,0,0,v_a[0]],\
             [0,1,0,v_a[1]],\
             [0,0,1,v_a[2]],\
             [0,0,0,1]])

        ## compute new vector for X-rotation matrix
        m_xyz_p = m_Rotate_Trans * m_xyz
        v_xyz_p = np.array(m_xyz_p.T)[0]
        f_x_p = v_xyz_p[0]
        f_y_p = v_xyz_p[1]
        f_z_p = v_xyz_p[2]        

        ###############################

        ## If not the X-axis as indicated by 0 length along Y-axis and Z-axis
        ## Needed or results in divide by 0 error
        if(f_y_p**2 + f_z_p**2):
            sin_X_axis = f_y_p / np.sqrt(f_y_p**2+f_z_p**2)
            cos_X_axis = f_z_p / np.sqrt(f_y_p**2+f_z_p**2)
        else:
            sin_X_axis = float(0.0)
            cos_X_axis = float(1.0)

        ## Establish matrix for rotating all points about X-axis
        ## such that vector 'ab' lies in XZ-plane
        m_Rotate_X = np.matrix(\
            [[1,0,0,0],\
             [0,cos_X_axis,-sin_X_axis,0],\
             [0,sin_X_axis,cos_X_axis,0],\
             [0,0,0,1]])
        ## establish inverse matrix (to save time vs. 'np.inverse(m_Rotate_X_Inv)')
        ## to rotate points back again at end of process
        m_Rotate_X_Inv = np.matrix(\
            [[1,0,0,0],\
             [0,cos_X_axis,sin_X_axis,0],\
             [0,-sin_X_axis,cos_X_axis,0],\
             [0,0,0,1]])

        ## compute new vector for Y-rotation matrix
        m_xyz_pp = m_Rotate_X * m_xyz_p
        v_xyz_pp = np.array(m_xyz_pp.T)[0]
        f_x_pp = v_xyz_pp[0]
        f_y_pp = v_xyz_pp[1]
        f_z_pp = v_xyz_pp[2] 

        ###############################
        
        ## If not the Y-axis as indicated by 0 length along X-axis and Z-axis
        ## Needed or results in divide by 0 error
        if(f_x_pp**2 + f_z_pp**2):
            sin_Y_axis = f_x_pp / np.sqrt(f_x_pp**2+f_z_pp**2)
            cos_Y_axis = f_z_pp / np.sqrt(f_x_pp**2+f_z_pp**2)
        else:
            sin_Y_axis = float(0.0)
            cos_Y_axis = float(1.0)

        ## Establish matrix for rotating all points about Y-axis
        ## such that vector 'ab' lies along Z-axis
        m_Rotate_Y = np.matrix(\
            [[cos_Y_axis,0,-sin_Y_axis,0],\
             [0,1,0,0],\
             [sin_Y_axis,0,cos_Y_axis,0],\
             [0,0,0,1]])
        ## establish inverse matrix (to save time vs. 'np.inverse(m_Rotate_Y_Inv)')
        ## to rotate points back again at end of process
        m_Rotate_Y_Inv = np.matrix(\
            [[cos_Y_axis,0,sin_Y_axis,0],\
             [0,1,0,0],\
             [-sin_Y_axis,0,cos_Y_axis,0],\
             [0,0,0,1]])

        ## compute new vector for Z-rotation matrix (though not needed)
        m_xyz_ppp = m_Rotate_Y * m_xyz_pp
        v_xyz_ppp = np.array(m_xyz_ppp.T)[0]
        f_x_ppp = v_xyz_ppp[0]
        f_y_ppp = v_xyz_ppp[1]
        f_z_ppp = v_xyz_ppp[2]

        ###############################
        
        sin_Z_axis = np.sin(float(f_degree)*np.pi/180.0)
        cos_Z_axis = np.cos(float(f_degree)*np.pi/180.0)

        ## Establish matrix for rotating all points about Z-axis
        ## such that the actual rotation by 'i_degrees' takes place
        m_Rotate_Z = np.matrix(\
            [[cos_Z_axis,-sin_Z_axis,0,0],\
             [sin_Z_axis,cos_Z_axis,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        m_Rotate_Z_Inv = np.matrix(\
            [[cos_Z_axis,sin_Z_axis,0,0],\
             [-sin_Z_axis,cos_Z_axis,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])

        print(' sin_X_axis = ' + str(sin_X_axis))
        print(' cos_X_axis = ' + str(cos_X_axis))
        print(' sin_Y_axis = ' + str(sin_Y_axis))
        print(' cos_Y_axis = ' + str(cos_Y_axis))
        print(' sin_Z_axis = ' + str(sin_Z_axis))
        print(' cos_Z_axis = ' + str(cos_Z_axis))
        
        ## Combine rotation transformation to be applied to points
        self.rotationMatrix = m_Rotate_Trans_Inv * m_Rotate_X_Inv * m_Rotate_Y_Inv * m_Rotate_Z * m_Rotate_Y * m_Rotate_X * m_Rotate_Trans

    def establish_scale_matrix(self, i_steps, v_scale, v_center):
        print(' Establishing scale matrix ')

        f_steps = float(i_steps)

        v_inc_scale = [1.0,1.0,1.0]
        v_inc_scale[0] = np.power(v_scale[0], 1.0/f_steps)
        v_inc_scale[1] = np.power(v_scale[1], 1.0/f_steps)
        v_inc_scale[2] = np.power(v_scale[2], 1.0/f_steps)
        print(' f_steps = ' + str(f_steps))
        print(' v_scale = ' + str(v_scale))
        print(' v_inc_scale = ' + str(v_inc_scale))

        ## Establish matrix for translating all points
        ## such that point 'a' lies at origin
        m_Scale_Trans = np.matrix(\
            [[1,0,0,-v_center[0]],\
             [0,1,0,-v_center[1]],\
             [0,0,1,-v_center[2]],\
             [0,0,0,1]])
        ## establish inverse matrix (to save time vs. 'np.inverse(m_Scale_Trans)')
        ## to translate points back again at end of process
        m_Scale_Trans_Inv = np.matrix(\
            [[1,0,0,v_center[0]],\
             [0,1,0,v_center[1]],\
             [0,0,1,v_center[2]],\
             [0,0,0,1]])
        ## establish matrix to perform actual scaling
        ## about origin
        m_Scale_Size = np.matrix(\
            [[v_inc_scale[0],0,0,0],\
             [0,v_inc_scale[1],0,0],\
             [0,0,v_inc_scale[2],0],\
             [0,0,0,1]])

        ## Combine translation transformation to be applied to points
        self.scaleMatrix = m_Scale_Trans_Inv * m_Scale_Size * m_Scale_Trans

    def establish_translation_matrix(self, i_steps, v_trans):
        print(' Establishing translation matrix ')

        f_steps = float(i_steps)

        v_inc_trans = [1.0, 1.0, 1.0]
        v_inc_trans[0] = v_trans[0]/f_steps
        v_inc_trans[1] = v_trans[1]/f_steps
        v_inc_trans[2] = v_trans[2]/f_steps
        print(' f_steps = ' + str(f_steps))
        print(' v_trans = ' + str(v_trans))
        print(' v_inc_trans = ' + str(v_inc_trans))

        ## Establish matrix for translating all points
        m_Trans = np.matrix(\
            [[1,0,0,v_inc_trans[0]],\
             [0,1,0,v_inc_trans[1]],\
             [0,0,1,v_inc_trans[2]],\
             [0,0,0,1]])

        ## Rename translation matrix for consistancy
        self.translationMatrix = m_Trans

    def establish_fly_matrix(self, i_steps, v_start, v_stop):
        print(' Establishing translation matrix ')

        f_steps = float(i_steps)

        v_inc_fly = [1.0, 1.0, 1.0]

        v_fly = [v_stop[0]-v_start[0], v_stop[1]-v_start[1], v_stop[2]-v_start[2]]
        v_inc_fly = [1.0, 1.0, 1.0]
        v_inc_fly[0] = v_fly[0]/f_steps
        v_inc_fly[1] = v_fly[1]/f_steps
        v_inc_fly[2] = v_fly[2]/f_steps
        print(' f_steps = ' + str(f_steps))
        print(' v_fly = ' + str(v_fly))
        print(' v_inc_fly = ' + str(v_inc_fly))

        ## Establish matrix for translating all points
        m_Fly = np.matrix(\
            [[1,0,0,v_inc_fly[0]],\
             [0,1,0,v_inc_fly[1]],\
             [0,0,1,v_inc_fly[2]],\
             [0,0,0,1]])

        ## Rename translation matrix for consistancy
        self.flyMatrix = m_Fly        



