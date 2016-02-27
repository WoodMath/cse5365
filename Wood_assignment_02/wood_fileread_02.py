# Wood, Jeff
# 100-103-5461
# 2016-03-02
# Assignment_02
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
import numpy as np
from numpy.linalg import inv

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

class mesh:
    def __init__(self):
        self.vertices=[]
        self.faces=[]
        self.wx=[]
        self.wy=[]
        self.vx=[]
        self.vy=[]
        self.filename=None
        self.coordinates=[]
        self.vMat=[]
        self.sMat=[]
        self.wMat=[]
        self.mMat=[]
        self.StackMatrix=np.matrix([[1,0,0,0],\
                                    [0,1,0,0],\
                                    [0,0,1,0],\
                                    [0,0,0,1]])
        self.bounding=[]
        self.box=[]
    def set_file(self,filename):
        self.vertices=[]
        self.faces=[]
        self.wx=[]
        self.wy=[]
        self.vx=[]
        self.vy=[]
        self.filename=filename
        self.coordinates=[]
        self.vMat=[]
        self.sMat=[]
        self.wMat=[]
        self.mMat=[]
        self.StackMatrix=np.matrix([[1,0,0,0],\
                                    [0,1,0,0],\
                                    [0,0,1,0],\
                                    [0,0,0,1]])
        self.bounding=[]
        self.box=[]
    def add_vertex(self,vertex):
        self.vertices.append(vertex)
    def add_face(self,face):
        self.faces.append(face)
    def add_window(self,window):
        self.wx=[window[0],window[2]]
        self.wy=[window[1],window[3]]
    def add_viewport(self,viewport):
        self.vx=[viewport[0],viewport[2]]
        self.vy=[viewport[1],viewport[3]]
        self.bounding.append([viewport[0],viewport[1],0.0,1.0])
        self.bounding.append([viewport[2],viewport[1],0.0,1.0])
        self.bounding.append([viewport[2],viewport[3],0.0,1.0])
        self.bounding.append([viewport[0],viewport[3],0.0,1.0])
        self.bounding.append([viewport[0],viewport[1],0.0,1.0])

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
    def establish_matrices(self):
        self.vMat=np.matrix([[1,0,0,self.vx[0]],\
                            [0,1,0,self.vy[0]],\
                            [0,0,1,0],\
                            [0,0,0,1]])
        self.sMat=np.matrix([[(self.vx[1]-self.vx[0])/(self.wx[1]-self.wx[0]),0,0,0],\
                            [0,(self.vy[1]-self.vy[0])/(self.wy[1]-self.wy[0]),0,0],\
                            [0,0,1,0],\
                            [0,0,0,1]])
        self.wMat=np.matrix([[1,0,0,-self.wx[0]],\
                            [0,1,0,-self.wy[0]],\
                            [0,0,1,0],\
                            [0,0,0,1]])
        self.tMat=np.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1]])
 #       self.mMat=self.vMat*self.sMat*self.wMat*self.tMat;
        self.mMat=self.vMat*self.sMat*self.wMat;
        self.vertices=np.matrix(self.vertices)
    def establish_coordinates(self,iWidth,iHeight):
        self.tMat = np.matrix([[float(iWidth),0,0,0],[0,float(iHeight),0,0],[0,0,1,0],[0,0,0,1]])
        self.tMat = self.tMat * np.matrix([[1,0,0,0],[0,-1,0,1],[0,0,1,0],[0,0,0,1]])

        # Transform vertices
        self.coordinates = self.tMat * self.mMat * np.transpose(np.matrix(self.vertices))
        self.coordinates = np.transpose(self.coordinates)
        # Transform viewport box
        self.box = self.tMat * np.transpose(np.matrix(self.bounding))
        self.box = np.transpose(self.box)
        
    def establish_rotation_matrices(self, i_divs, v_a, v_b, i_degree):
        print(' establishing rotation matrices ')
        v_a = np.array(v_a)
        v_b = np.array(v_b)
        v_ab = v_b-v_a
        f_x = v_ab[0]
        f_y = v_ab[1]
        f_z = v_ab[2]


        m_Rotate_Trans = np.matrix(\
            [[1,0,0,-v_a[0]],\
             [0,1,0,-v_a[1]],\
             [0,0,1,-v_a[2]],\
             [0,0,0,1]])
        m_Rotate_Trans_Inv = np.matrix(\
            [[1,0,0,v_a[0]],\
             [0,1,0,v_a[1]],\
             [0,0,1,v_a[2]],\
             [0,0,0,1]])
            
        sin_X_axis = f_y / np.sqrt(f_y**2+f_z**2)
        cos_X_axis = f_z / np.sqrt(f_y**2+f_z**2)
        sin_Y_axis = f_x / np.sqrt(f_x**2+f_z**2)
        cos_Y_axis = f_z / np.sqrt(f_x**2+f_z**2)
        sin_Z_axis = np.sin(float(i_degree)*np.pi/180.0)
        cos_Z_axis = np.cos(float(i_degree)*np.pi/180.0)

        m_Rotate_X = np.matrix(\
            [[1,0,0,0],\
             [0,cos_X_axis,-sin_X_axis,0],\
             [0,sin_X_axis,cos_X_axis,0],\
             [0,0,0,1]])
        m_Rotate_X_Inv = np.matrix(\
            [[1,0,0,0],\
             [0,cos_X_axis,sin_X_axis,0],\
             [0,-sin_X_axis,cos_X_axis,0],\
             [0,0,0,1]])

        m_Rotate_Y = np.matrix(\
            [[cos_Y_axis,0,-sin_Y_axis,0],\
             [0,1,0,0],\
             [sin_Y_axis,0,cos_Y_axis,0],\
             [0,0,0,1]])
        m_Rotate_Y_Inv = np.matrix(\
            [[cos_Y_axis,0,sin_Y_axis,0],\
             [0,1,0,0],\
             [-sin_Y_axis,0,cos_Y_axis,0],\
             [0,0,0,1]])

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

    def establish_scale_matrices(self, i_divs, v_scale, v_center):
        print(' establishing scale matrices ')

        m_Scale_Trans = np.matrix(\
            [[1,0,0,-v_center[0]],\
             [0,1,0,-v_center[1]],\
             [0,0,1,-v_center[2]],\
             [0,0,0,1]])
        m_Scale_Trans_Inv = np.matrix(\
            [[1,0,0,v_center[0]],\
             [0,1,0,v_center[1]],\
             [0,0,1,v_center[2]],\
             [0,0,0,1]])
        m_Scale_Size = np.matrix(\
            [[v_scale[0],0,0,0],\
             [0,v_scale[1],0,0],\
             [0,0,v_scale[2],0],\
             [0,0,0,1]])

## Code used to test functionality
#m=mesh()
#m.set_file('/home/jeff/Dropbox/cse5365/assignments/Wood_assignment_01/pyramid_01.txt')
#m.set_file('/home/jeff/Dropbox/cse5365/assignments/Wood_assignment_01/teapot_01.txt')
#m.load()
#m.establish_matrices()
#m.establish_coordinates(500,500)
