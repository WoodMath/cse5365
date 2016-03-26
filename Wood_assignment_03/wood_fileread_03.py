# Wood, Jeff
# 100-103-5461
# 2016-04-08
# Assignment_03

#!/~/anaconda3/bin/python3.5

#   From:
#       http://stackoverflow.com/questions/15599639/whats-perfect-counterpart-in-python-for-while-not-eof
#       http://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
#       http://stackoverflow.com/questions/7118276/how-to-remove-specific-element-in-an-array-using-python
#       http://stackoverflow.com/questions/379906/parse-string-to-float-or-int
#       http://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index-in-python
#       http://docs.scipy.org/doc/numpy/reference/generated/numpy.dot.html#numpy.dot
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.vectorize.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.matrix.transpose.html
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.array.html
#
#       http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_polygon.html
#       http://zetcode.com/gui/tkinter/drawing/
#       http://effbot.org/tkinterbook/canvas.htm
#
#       https://docs.scipy.org/doc/numpy-dev/user/quickstart.html
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.array.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.matrix.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.multiply.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.matrix.transpose.html
#
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.power.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.sqrt.html
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.linalg.inv.html
#
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.sin.html
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.cos.html
#
#       http://effbot.org/pyfaq/how-do-i-copy-an-object-in-python.htm
#
#       http://codereview.stackexchange.com/questions/43928/algorithm-to-get-an-arbitrary-perpendicular-vector

import numpy as np
import copy
from numpy.linalg import inv
from numpy import linalg as LA

class number_range:
    def __init__(self,vMin,vMax):
        self.min=vMin
        self.max=vMax
    def set_number_range(self,vMin,vMax):
        self.min=vMin
        self.max=vMax        

def single_int(passed_int):
    return int(passed_int)
def single_int_less_one(passed_int):
    return int(passed_int)-1
def single_float(passed_float):
    return float(passed_float)

vect_int=np.vectorize(int)
vect_int_less_one=np.vectorize(single_int_less_one)
vect_float=np.vectorize(float)

def iszero(numeric):
    if abs(numeric)*500==0 :
        return True
    else:
        return False
    
def vector_projection(vVectorU, vVectorV):
    ## Returns projection of vector U along vector V
    vDotUV = np.dot(np.array(vVectorU), np.array(vVectorV))
    vDotVV = np.dot(np.array(vVectorV), np.array(vVectorV))
    vReturn = np.array(vVectorV)*vDotUV/vDotVV
#    return vReturn
    return vDotUV/vDotVV

def old_vector_perpendicular(u):
    v=np.array(u)
    if iszero(v[0]) and iszero(v[1]):
        if iszero(v[2]):
            # v is Vector(0, 0, 0)
            raise ValueError('zero vector')

        # v is Vector(0, 0, v.z)
        return np.array([0,1,0])

    return np.array([-v[1], v[0], 0])

def vector_perpendicular(u):
    v=np.array(u)
    r""" Finds an arbitrary perpendicular vector to *v*."""
    # for two vectors (x, y, z) and (a, b, c) to be perpendicular,
    # the following equation has to be fulfilled
    #     0 = ax + by + cz

    # x = y = z = 0 is not an acceptable solution
    if v[0] == v[1] == v[2] == 0:
        raise ValueError('zero-vector')

    # If one dimension is zero, this can be solved by setting that to
    # non-zero and the others to zero. Example: (4, 2, 0) lies in the
    # x-y-Plane, so (0, 0, 1) is orthogonal to the plane.
    if v[0] == 0:
        return np.array([1, 0, 0])
    if v[1] == 0:
        return np.array([0, 1, 0])
    if v[2] == 0:
        return np.array([0, 0, 1])

    # arbitrarily set a = b = 1
    # then the equation simplifies to
    #     c = -(x + y)/z
#    return Vector(1, 1, -1.0 * (v.x + v.y) / v.z)
    return np.array([1,1,-1*(v[0]+v[1])/v[2]])

#old_vector_perpendicular(np.array([1,1,1]))


def vector_rotate(vVector0, vVector1):
    ## Returns the matrix necessary to rotate a vector vVector0 onto vVector1 

    v0 = copy.copy(np.array(vVector0))
    v1 = copy.copy(np.array(vVector1))
    fLength0 = LA.norm(v0)
    fLength1 = LA.norm(v1)
    v0 = np.array(vVector0)/fLength0
    v1 = np.array(vVector1)/fLength1


    v0_len = LA.norm(v0)
    v1_len = LA.norm(v1)

    print('v0_len = ', v0_len)
    print('v1_len = ', v1_len)
    
    
    ## Assign v0 as vU axis
    vU = copy.copy(v0)
    ## Make v1 span vU and vV axis and caluculate vV = v1-vU


    vW_nn = np.cross(v0,v1)
    vW_len = LA.norm(vW_nn)
    if not(vW_len):
        ## For special case when v0 and v1 are co-linear
        ## Set arbitrary rotation axis (vW)
        vW_nn = old_vector_perpendicular(v0)
        vW_len = LA.norm(vW_nn)
        
    vW = vW_nn/vW_len        
    vV_nn = np.cross(vW,vU)
    vV_len = LA.norm(vV_nn)
    vV = vV_nn/vV_len

    vU_len = LA.norm(vU)
    vV_len = LA.norm(vV)
    vW_len = LA.norm(vW)

    print('vU_len = ', vU_len)
    print('vV_len = ', vV_len)
    print('vW_len = ', vW_len)
    


    print('v0 = ', end='')
    print(v0)
    print('v1 = ', end='')
    print(v1)

    print('vU = ', end='')
    print(vU)
    print('vV = ', end='')
    print(vV)
    print('vW = ', end='')
    print(vW)
    
    if(np.dot(vU,vV) or np.dot(vU,vW)):
        raise ValueError('Vectors are not orthogonal')

    vAxis = vW

    ## Get horizontal and vertical components of v1 with respect to v0
    fU = vector_projection(v1,vU)
    fV = vector_projection(v1,vV)

    print('fU = ', end='')
    print(fU)
    print('fV = ', end='')
    print(fV)

        ## Assign Sin outputs based on results
    sin_Z_axis = fV / np.sqrt(fU**2+fV**2)
    cos_Z_axis = fU / np.sqrt(fU**2+fV**2)
#    else:
#        sin_Z_axis = float(0.0)
#        cos_Z_axis = float(1.0)



    ## Establish the rotation matrices
    
    f_x = vAxis[0]
    f_y = vAxis[1]
    f_z = vAxis[2]


    ## If not the X-axis as indicated by 0 length along Y-axis and Z-axis
    ## Needed or results in divide by 0 error
    if(f_y**2 + f_z**2):
        sin_X_axis = f_y / np.sqrt(f_y**2+f_z**2)
        cos_X_axis = f_z / np.sqrt(f_y**2+f_z**2)
    else:
        sin_X_axis = float(0.0)
        cos_X_axis = float(1.0)

    ## If not the Y-axis as indicated by 0 length along X-axis and Z-axis
    ## Needed or results in divide by 0 error
    if(f_x**2 + f_z**2):
        sin_Y_axis = f_x / np.sqrt(f_x**2+f_z**2)
        cos_Y_axis = f_z / np.sqrt(f_x**2+f_z**2)
    else:
        sin_Y_axis = float(0.0)
        cos_Y_axis = float(1.0)
            
    ## If not the Y-axis as indicated by 0 length along X-axis and Z-axis
    ## Needed or results in divide by 0 error

    print(' sin_X_axis = ' + str(sin_X_axis))
    print(' cos_X_axis = ' + str(cos_X_axis))
    print(' sin_Y_axis = ' + str(sin_Y_axis))
    print(' cos_Y_axis = ' + str(cos_Y_axis))
    print(' sin_Z_axis = ' + str(sin_Z_axis))
    print(' cos_Z_axis = ' + str(cos_Z_axis))

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


    ## Due to Gimball lock will need to reverse angle if negative
    v_Test = m_Rotate_Y * m_Rotate_X * np.transpose(np.matrix([v0[0],v0[1],v0[2],1]));
    v_Test = np.array(v_Test.T)[0]

    print('v_Test = ',end='')
    print(v_Test)
#    print('v_Test[1][0] = ',end='')
#    print(v_Test[1][0])    

    ## Due to Gimball lock will need to reverse angle if negative Y-coordinate for Z-rotation
    if(v_Test[1]<0):
        print(' m_Rotate_Z = ')
        print(m_Rotate_Z)

        m_Rotate_Z = np.transpose(m_Rotate_Z)
        m_Rotate_Z_Inv = np.transpose(m_Rotate_Z_Inv)

        print(' m_Rotate_Z = ')
        print(m_Rotate_Z)

#        m_Temp = m_Rotate_Z
#        m_Rotate_Z = m_Rotate_Z_Inv
#        m_Rotate_Z_Inv = m_Temp


    ## Combine rotation transformation to be applied to points
    rotationMatrix = m_Rotate_X_Inv * m_Rotate_Y_Inv * m_Rotate_Z * m_Rotate_Y * m_Rotate_X


    checkResult = rotationMatrix*np.transpose(np.matrix([[v0[0],v0[1],v0[2],1]]))



    print(' m_Rotate_X = ')
    print(m_Rotate_X)

    print(' m_Rotate_Y = ')
    print(m_Rotate_Y)

    print(' m_Rotate_Z = ')
    print(m_Rotate_Z)

    print(' checkResult = ',end='')
    print(np.array(np.transpose(checkResult)))
    print(' v1 = ',end='')
    print(v1)

    return rotationMatrix

print(vector_rotate([1,0,0],[0,-1,0]))

class mesh:
    def __init__(self):
        self.vertices=[]
        self.transformed_vertices=[]
        self.stack=np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
        self.faces=[]
        self.wu=[]
        self.wv=[]
        self.wn=[]
        self.vx=[]
        self.vy=[]
        self.filename=[]
        self.coordinates=[]
        self.world2viewMatrix=[]
        self.view2screenMatrix=[]
        self.stackMatrix=np.matrix([[1,0,0,0],\
                                    [0,1,0,0],\
                                    [0,0,1,0],\
                                    [0,0,0,1]])
        self.bounding=[]
        self.box=[]
        self.step=0
        self.steps=0
        self.vrp=None
        self.vpn=None
        self.vup=None
        self.prp=None

    def set_file(self,filename):
        self.vertices=[]
        self.transformed_vertices=[]
        self.stack=np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
        self.faces=[]
        self.wu=[]
        self.wv=[]
        self.wn=[]        
        self.vx=[]
        self.vy=[]
        self.filename=filename
        self.coordinates=[]
        self.world2viewMatrix=[]
        self.view2screenMatrix=[]
        self.stackMatrix=np.matrix([[1,0,0,0],\
                                    [0,1,0,0],\
                                    [0,0,1,0],\
                                    [0,0,0,1]])
        self.bounding=[]
        self.box=[]
        self.step=0
        self.steps=0
        self.vrp=None
        self.vpn=None
        self.vup=None
        self.prp=None

    def add_vertex(self,vertex):
        self.vertices.append(vertex)
    def add_face(self,face):
        self.faces.append(face)
    def add_window(self,window):
        self.wu=[window[0],window[1]]
        self.wv=[window[2],window[3]]
        self.wn=[window[4],window[5]]        
    def add_viewport(self,viewport):
        self.vx=[viewport[0],viewport[2]]
        self.vy=[viewport[1],viewport[3]]
        self.bounding.append([viewport[0],viewport[1],0.0,1.0])
        self.bounding.append([viewport[2],viewport[1],0.0,1.0])
        self.bounding.append([viewport[2],viewport[3],0.0,1.0])
        self.bounding.append([viewport[0],viewport[3],0.0,1.0])
        self.bounding.append([viewport[0],viewport[1],0.0,1.0])
    def add_vrp(self,vrp):
        self.vrp = vrp
    def add_vpn(self,vpn):
        self.vpn = vpn
    def add_vup(self,vup):
        self.vup = vup
    def add_prp(self,prp):
        self.prp = prp

    def load(self):
        with open(self.filename) as openfileobject:
            for line in openfileobject:
                line_parsed=line.split()
                if(len(line_parsed)>0):
                    line_type=line_parsed[0]
                    line_parsed.pop(0)
                    if(line_type=='v'):
                        line_parsed.append('1.0')
                        line_parsed=vect_float(line_parsed)
                        self.add_vertex(line_parsed)
                    if(line_type=='f'):
                        line_parsed=vect_int_less_one(line_parsed[:])
                        self.add_face(line_parsed)
                    if(line_type=='w'):
                        line_parsed=vect_float(line_parsed[:])
                        self.add_window(line_parsed)
                    if(line_type=='s'):
                        line_parsed=vect_float(line_parsed[:])
                        self.add_viewport(line_parsed)
                    if(line_type=='r'):
                        line_parsed=vect_int(line_parsed[:])
                        self.add_vrp(line_parsed)
                    if(line_type=='n'):
                        line_parsed=vect_int(line_parsed[:])
                        self.add_vpn(line_parsed)
                    if(line_type=='u'):
                        line_parsed=vect_int(line_parsed[:])
                        self.add_vup(line_parsed)
                    if(line_type=='p'):
                        line_parsed=vect_int(line_parsed[:])
                        self.add_prp(line_parsed)
                        
    def establish_matrices(self):
        print(' Establishing matrices ')
        
        stepOneMatrix=np.matrix(\
            [[1,0,0,-self.vrp[0]],\
             [0,1,0,-self.vrp[1]],\
             [0,0,1,-self.vrp[2]],\
             [0,0,0,1]])
        vMat=np.matrix(\
            [[1,0,0,self.vx[0]],\
             [0,1,0,self.vy[0]],\
             [0,0,1,0],[0,0,0,1]])
        sMat=np.matrix(\
            [[(self.vx[1]-self.vx[0])/(self.wu[1]-self.wu[0]),0,0,0],\
             [0,(self.vy[1]-self.vy[0])/(self.wv[1]-self.wv[0]),0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        wMat=np.matrix(\
            [[1,0,0,-self.wu[0]],\
             [0,1,0,-self.wv[0]],\
             [0,0,1,0],\
             [0,0,0,1]])
        tMat=np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,0,1]])
        self.world2viewMatrix = vMat * sMat * wMat;
        self.vertices=np.matrix(self.vertices)

        ## Do not transfer from 'object space' into 'world space' until
        ## 'establish_matrices' called from 'load_file' in 'wood_widgets_02.py'
        self.transformed_vertices=copy.copy(self.vertices)

    def establish_coordinates(self,iWidth,iHeight):
        self.view2screenMatrix = np.matrix([[float(iWidth),0,0,0],[0,float(iHeight),0,0],[0,0,1,0],[0,0,0,1]])
        self.view2screenMatrix  = self.view2screenMatrix  * np.matrix([[1,0,0,0],[0,-1,0,1],[0,0,1,0],[0,0,0,1]])

        print(' Establishing coordinates ')

        # Transform vertices into coordinates
        self.coordinates = self.view2screenMatrix * self.world2viewMatrix * np.transpose(np.matrix(self.transformed_vertices))
        self.coordinates = np.transpose(self.coordinates)

        # Transform viewport box
        self.box = self.view2screenMatrix * np.transpose(np.matrix(self.bounding))
        self.box = np.transpose(self.box)

        
    def establish_rotation_matrices(self, i_steps, v_a, v_b, i_degree):
        # Establish the rotation matrices
        
        print(' Establishing rotation matrices ')
        v_a = np.array(v_a)
        v_b = np.array(v_b)
        v_ab = v_b-v_a
        f_x = v_ab[0]
        f_y = v_ab[1]
        f_z = v_ab[2]

        f_degree = float(i_degree)
        f_steps = float(i_steps)
        f_degree = f_degree / f_steps

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

        ## If not the X-axis as indicated by 0 length along Y-axis and Z-axis
        ## Needed or results in divide by 0 error
        if(f_y**2 + f_z**2):
            sin_X_axis = f_y / np.sqrt(f_y**2+f_z**2)
            cos_X_axis = f_z / np.sqrt(f_y**2+f_z**2)
        else:
            sin_X_axis = float(0.0)
            cos_X_axis = float(1.0)

        ## If not the Y-axis as indicated by 0 length along X-axis and Z-axis
        ## Needed or results in divide by 0 error
        if(f_x**2 + f_z**2):
            sin_Y_axis = f_x / np.sqrt(f_x**2+f_z**2)
            cos_Y_axis = f_z / np.sqrt(f_x**2+f_z**2)
        else:
            sin_Y_axis = float(0.0)
            cos_Y_axis = float(1.0)
            
        sin_Z_axis = np.sin(float(f_degree)*np.pi/180.0)
        cos_Z_axis = np.cos(float(f_degree)*np.pi/180.0)

        print(' sin_X_axis = ' + str(sin_X_axis))
        print(' cos_X_axis = ' + str(cos_X_axis))
        print(' sin_Y_axis = ' + str(sin_Y_axis))
        print(' cos_Y_axis = ' + str(cos_Y_axis))
        print(' sin_Z_axis = ' + str(sin_Z_axis))
        print(' cos_Z_axis = ' + str(cos_Z_axis))

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

        ## Establish matrix for rotating all points about Z-axis
        ## such that the actual rotation by 'i_degrees' takes place
        m_Rotate_Z = np.matrix(\
            [[cos_Z_axis,-sin_Z_axis,0,0],\
             [sin_Z_axis,cos_Z_axis,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
#        m_Rotate_Z_Inv = np.matrix(\
#            [[cos_Z_axis,sin_Z_axis,0,0],\
#             [-sin_Z_axis,cos_Z_axis,0,0],\
#             [0,0,1,0],\
#             [0,0,0,1]])

        ## Combine rotation transformation to be applied to points
        rotationMatrix = m_Rotate_Trans_Inv * m_Rotate_X_Inv * m_Rotate_Y_Inv * m_Rotate_Z * m_Rotate_Y * m_Rotate_X * m_Rotate_Trans

        ## Transform vertices into coordinates
        self.transformed_vertices = rotationMatrix * np.transpose(np.matrix(self.transformed_vertices))
        self.transformed_vertices = np.transpose(self.transformed_vertices)

    def establish_scale_matrices(self, i_steps, v_scale, v_center):
        print(' Establishing scale matrices ')

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
        scaleMatrix = m_Scale_Trans_Inv * m_Scale_Size * m_Scale_Trans

        ## Transform vertices into coordinates
        self.transformed_vertices = scaleMatrix * np.transpose(np.matrix(self.transformed_vertices))
        self.transformed_vertices = np.transpose(self.transformed_vertices)


    def establish_translation_matrices(self, i_steps, v_trans):
        print(' Establishing translation matrices ')

        f_steps = float(i_steps)

        v_inc_trans = [1.0,1.0,1.0]
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
        transMatrix = m_Trans

        ## Transform vertices into coordinates
        self.transformed_vertices = transMatrix * np.transpose(np.matrix(self.transformed_vertices))
        self.transformed_vertices = np.transpose(self.transformed_vertices)

## Code used to test functionality
#m=mesh()
#m.set_file('/home/jeff/Dropbox/cse5365/assignments/Wood_assignment_01/pyramid_01.txt')
#m.set_file('/home/jeff/Dropbox/cse5365/assignments/Wood_assignment_01/teapot_01.txt')
#m.load()
#m.establish_matrices()
#m.establish_coordinates(500,500)


