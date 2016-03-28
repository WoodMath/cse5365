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

class viewTransform:
    def __init__(self):
        self.parent = self
        self.vU = []
        self.vV = []
        self.vN = []
        self.vNDCx = [-1,1]
        self.vNDCy = [-1,1]
        self.vNDCz = [0,1]
        self.updateNDC()
    def updateNDC(self):
        self.fNDCx = self.vNDCx[1]-self.vNDCx[0]
        self.fNDCy = self.vNDCy[1]-self.vNDCy[0]
        self.fNDCz = self.vNDCz[1]-self.vNDCz[0]
        
    def array2matrix(self,v_Array):
        vArray = np.array(v_Array)
        mReturn = np.transpose(np.matrix(vArray))
        return mReturn
    def matrix2array(self,m_Matrix):
        mMatrix = np.matrix(m_Matrix)
        vReturn = np.array(mMatrix.T)[0]
        return vReturn
    def arrayAdd1(self, v_Array):
        vArray = np.array(v_Array)
        vArray = np.append(vArray,1)
        return vArray
    def arrayRemove1(self, v_Array):
        vArray = np.array(v_Array)
        if(vArray[len(vArray)-1]==1):
            vReturn = np.delete(vArray,len(vArray)-1)
        else:
            vReturn = vArray
        return vReturn
    
    def transformVRP2Origin(self,v_VRP):
        vVRP = np.array(v_VRP)

        f_x = vVRP[0]
        f_y = vVRP[1]
        f_z = vVRP[2]

        m_Translate = np.matrix(\
            [[1,0,0,-f_x],\
             [0,1,0,-f_y],\
             [0,0,1,-f_z],\
             [0,0,0,1]])

        mReturn = m_Translate

        return mReturn
        
    def transformVPN2Z(self,v_VPN):
        vVPN = np.array(v_VPN)
        
        f_x = vVPN[0]
        f_y = vVPN[1]
        f_z = vVPN[2]
        v_xyz = np.array([f_x,f_y,f_z,1])
        m_xyz = np.transpose(np.matrix(v_xyz))

        ###############################

        ## If not the X-axis as indicated by 0 length along Y-axis and Z-axis
        ## Needed or results in divide by 0 error
        if(f_y**2 + f_z**2):
            sin_X_axis = f_y / np.sqrt(f_y**2+f_z**2)
            cos_X_axis = f_z / np.sqrt(f_y**2+f_z**2)
        else:
            sin_X_axis = float(0.0)
            cos_X_axis = float(1.0)
        
        ## Establish matrix for VPN about X-axis
        ## such that vector VPN lies in XZ-plane
        m_Rotate_X = np.matrix(\
            [[1,0,0,0],\
             [0,cos_X_axis,-sin_X_axis,0],\
             [0,sin_X_axis,cos_X_axis,0],\
             [0,0,0,1]])

        ## compute new vector for Y-rotation matrix
        m_xyz_p = m_Rotate_X * m_xyz
        v_xyz_p = np.array(m_xyz_p.T)[0]
        f_x_p = v_xyz_p[0]
        f_y_p = v_xyz_p[1]
        f_z_p = v_xyz_p[2]

        ###############################
        
        ## If not the Y-axis as indicated by 0 length along X-axis and Z-axis
        ## Needed or results in divide by 0 error
        if(f_x_p**2 + f_z_p**2):
            sin_Y_axis = f_x_p / np.sqrt(f_x_p**2+f_z_p**2)
            cos_Y_axis = f_z_p / np.sqrt(f_x_p**2+f_z_p**2)
        else:
            sin_Y_axis = float(0.0)
            cos_Y_axis = float(1.0)

        ## Establish matrix for VPN about Y-axis
        ## such that vector VPN lies along Z-axis
        m_Rotate_Y = np.matrix(\
            [[cos_Y_axis,0,-sin_Y_axis,0],\
             [0,1,0,0],\
             [sin_Y_axis,0,cos_Y_axis,0],\
             [0,0,0,1]])

        ## compute new vector for Z-rotation matrix (though not needed)
        m_xyz_p = m_Rotate_X * m_xyz
        v_xyz_p = np.array(m_xyz_p.T)[0]
        f_x_p = v_xyz_p[0]
        f_y_p = v_xyz_p[1]
        f_z_p = v_xyz_p[2]

        ###############################
        
        ## Combine rotation transformation to be applied to vector
        mReturn = m_Rotate_Y * m_Rotate_X

        return mReturn
    
    def transformVUP2YZ(self,v_VUP):
        vVUP = np.array(v_VUP)
        
        f_x = vVUP[0]
        f_y = vVUP[1]
        f_z = vVUP[2]
        v_xyz = np.array([f_x,f_y,f_z,1])
        m_xyz = np.transpose(np.matrix(v_xyz))

        ###############################

        ## If not the Z-axis as indicated by 0 length along X-axis and Y-axis
        ## Needed or results in divide by 0 error
        if(f_x**2 + f_y**2):
            sin_Z_axis = f_x / np.sqrt(f_x**2+f_y**2)
            cos_Z_axis = f_y / np.sqrt(f_x**2+f_y**2)
        else:
            sin_Z_axis = float(0.0)
            cos_Z_axis = float(1.0)
        
        ## Establish matrix for VUP about Z-axis
        ## such that vector VUP lies in YZ-plane
        m_Rotate_Z = np.matrix(\
            [[cos_Z_axis,-sin_Z_axis,0,0],\
             [sin_Z_axis,cos_Z_axis,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])

        ## compute new vector for Y-rotation matrix
        m_xyz_p = m_Rotate_Z * m_xyz
        v_xyz_p = np.array(m_xyz_p.T)[0]
        f_x_p = v_xyz_p[0]
        f_y_p = v_xyz_p[1]
        f_z_p = v_xyz_p[2]

        ###############################
                
        mReturn = m_Rotate_Z

        return mReturn

    def getUfromVPNandVUP(this,v_VPN,v_VUP):
        vVPN = np.array(v_VPN)
        vVUP = np.array(v_VUP)
        vU_nn = np.cross(vVUP,vVPN)
        vU_len = LA.norm(vU_nn)
        vU = vU_nn/vU_len
        return vU
    
    def getVfromVPNandU(this,v_VPN,v_U):
        vVPN = np.array(v_VPN)
        vU = np.array(v_U)
        vV_nn = np.cross(vVPN,vU)
        vV_len = LA.norm(vV_nn)
        vV = vV_nn/vV_len
        return vV

    def getUVfromVPNandVUP(this,v_VPN,v_VUP):
        vVPN = np.array(v_VPN)
        vVUP = np.array(v_VUP)
        vU_nn = np.cross(vVUP,vVPN)
        vU_len = LA.norm(vU_nn)
        vU = vU_nn/vU_len
        vV_nn = np.cross(vVPN,vU)
        vV_len = LA.norm(vV_nn)
        vV = vV_nn/vV_len
        return (vU,vV)

    def transformVRCshear(this,v_PRP,v_Dim_U,v_Dim_V):
        vPRP = np.array(v_PRP)
        vDim_U = np.array(v_Dim_U)
        vDim_V = np.array(v_Dim_V)
        fCW_U = (vDim_U[1]+vDim_U[0])/2
        fCW_V = (vDim_V[1]+vDim_V[0])/2
        fPRP_X = vPRP[0]
        fPRP_Y = vPRP[1]
        fPRP_Z = vPRP[2]
        
        fSh_X = -(fPRP_X - fCW_U)/fPRP_Z
        fSh_Y = -(fPRP_Y - fCW_V)/fPRP_Z

        mReturn = np.matrix(\
            [[1, 0, fSh_X, 0],\
             [0, 1, fSh_Y, 0],\
             [0, 0, 1, 0],\
             [0, 0, 0, 1]])

        return mReturn

    def transformVRCtranslate(this,v_Dim_U,v_Dim_V,v_Dim_N):
        vDim_U = np.array(v_Dim_U)
        vDim_V = np.array(v_Dim_V)
        vDim_N = np.array(v_Dim_N)
        fCW_U = (vDim_U[1]+vDim_U[0])/2
        fCW_V = (vDim_V[1]+vDim_V[0])/2
        fMin_N = vDim_N[0] if vDim_N[0] <= vDim_N[1] else vDim_N[1]
        fMin_N = vDim_N[0]
        
        mReturn = np.matrix(\
            [[1, 0, 0, -fCW_U],\
             [0, 1, 0, -fCW_V],\
             [0, 0, 1, -fMin_N],\
             [0, 0, 0, 1]])

        return mReturn

    def transformVRCscale(this,v_Dim_U,v_Dim_V,v_Dim_N):
        vDim_U = np.array(v_Dim_U)
        vDim_V = np.array(v_Dim_V)
        vDim_N = np.array(v_Dim_N)
        fScale_U = self.fNDCx/(vDim_U[1]-vDim_U[0])
        fScale_V = self.fNDCy/(vDim_V[1]-vDim_V[0])
        fScale_N = self.fNDCz/(vDim_N[1]-vDim_N[0])
        mReturn = np.matrix(\
            [[fScale_U, 0, 0, 0],\
             [0, fScale_V, 0, 0],\
             [0, 0, fScale_N, 0],\
             [0, 0, 0, 1]])

        return mReturn




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
        self.sx=[]
        self.sy=[]
        self.filename=[]
        self.coordinates=[]
        self.world2viewMatrix=[]
        self.view2screenMatrix=[]
        self.startMatrix=np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        self.stackMatrix=np.matrix(\
            [[1,0,0,0],\
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
        self.scaleMatrix=None
        self.rotationMatrix=None
        self.translationMatrix=None

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
        self.sx=[]
        self.sy=[]
        self.filename=filename
        self.coordinates=[]
        self.world2viewMatrix=[]
        self.view2screenMatrix=[]
        self.startMatrix=np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        self.stackMatrix=np.matrix(\
            [[1,0,0,0],\
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
        self.scaleMatrix=None
        self.rotationMatrix=None
        self.translationMatrix=None

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
    def resetStack(self):
        self.stackMatrix=np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
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

        self.sx = (self.vx[1]-self.vx[0])/(self.wu[1]-self.wu[0])
        self.sy = (self.vy[1]-self.vy[0])/(self.wv[1]-self.wv[0])

    def establish_coordinates(self,iWidth,iHeight):

        self.view2screenMatrix = np.matrix(\
            [[float(iWidth),0,0,0],\
             [0,float(iHeight),0,0],\
             [0,0,1,0],\
             [0,0,0,1]])

#        self.view2screenMatrix  = self.view2screenMatrix * np.matrix(\
#            [[ 1, 0, 0, 0],\
#             [ 0,-1, 0, 1],\
#             [ 0, 0, 1, 0],\
#             [ 0, 0, 0, 1]])

        print(' Establishing coordinates ')
        # Transform vertices into coordinates
        self.coordinates = self.view2screenMatrix * self.world2viewMatrix * self.stackMatrix * np.transpose(np.matrix(self.transformed_vertices))
        self.coordinates = np.transpose(self.coordinates)

        # Transform viewport box
        self.box = self.view2screenMatrix * np.transpose(np.matrix(self.bounding))
        self.box = np.transpose(self.box)
        
    def establish_view_matrix(self):
        print(' Establishing view matrix ')

        tObj = viewTransform()

        ##################################

        ## Translate VRP vector 2 origin (Step 1)
        self.step1Matrix = tObj.transformVRP2Origin(self.vrp)

        ## Test VRP vector [0,0,0]
        mTempVRP = tObj.array2matrix(tObj.arrayAdd1(self.vrp))
        mTempVRP = self.step1Matrix * mTempVRP
        vTempVRP = tObj.arrayRemove1(tObj.matrix2array(mTempVRP))
        print(' vTempVRP = ',end='')
        print(vTempVRP)
        
        ##################################

        ## Rotate VPN vector 2 Z-Axis (Step 2)
        self.step2Matrix = tObj.transformVPN2Z(self.vpn)

        ## Test new VPN vector [0,0,a]
        mTempVPN = tObj.array2matrix(tObj.arrayAdd1(self.vpn))
        mTempVPN = self.step2Matrix * mTempVPN
        vTempVPN = tObj.arrayRemove1(tObj.matrix2array(mTempVPN))
        print(' vTempVPN = ',end='')
        print(vTempVPN)

        ##################################
        
        ## Get new VUP vector
        mTempVUP = tObj.array2matrix(tObj.arrayAdd1(self.vup))
        mTempVUP = self.step2Matrix * mTempVUP
        vTempVUP = tObj.arrayRemove1(tObj.matrix2array(mTempVUP))

        ## Rotate new VUP vector 2 YZ-Plane (Step 3)
        self.step3Matrix = tObj.transformVUP2YZ(vTempVUP)

        ## Test new VUP vector [0,b,c]
        mTempVUP = tObj.array2matrix(tObj.arrayAdd1(vTempVUP))
        mTempVUP = self.step3Matrix * mTempVUP
        vTempVUP = tObj.arrayRemove1(tObj.matrix2array(mTempVUP))

        print(' vTempVUP = ',end='')
        print(vTempVUP)

        ##################################

        ## Define (W)indowed view volume
        v_Dim_U = self.wu
        v_Dim_V = self.wv
        v_Dim_N = self.wn

        ## Shear DOP = (PRP-CW) to be prallel to Z-Axis (Step 4)
        self.step4Matrix = tObj.transformVRCshear(self.prp,v_Dim_U,v_Dim_V)

        ## Test new VUP vector [CW_x,CW_y,PRP_z]
        mTempPRP = tObj.array2matrix(tObj.arrayAdd1(self.prp))
        mTempPRP = self.step4Matrix * mTempPRP
        vTempPRP = tObj.arrayRemove1(tObj.matrix2array(mTempPRP))

        print(' vTempPRP = ',end='')
        print(vTempPRP)

        ##################################

        ## Translate viewing volume to origin (Step 5)
        self.step5Matrix = tObj.transformVRCtranslate(v_Dim_U,v_Dim_V,v_Dim_N)

        ## Define Center of (W)indow
        fCW_U = (v_Dim_U[1]+v_Dim_U[0])/2
        fCW_V = (v_Dim_V[1]+v_Dim_V[0])/2
        fMin_N = v_Dim_N[0] if v_Dim_N[0] <= v_Dim_N[1] else v_Dim_N[1]
        fMin_N = v_Dim_N[0]
                
        ## Test new CW vector [0,0,0]
        mTempUVN = tObj.array2matrix(tObj.arrayAdd1([fCW_U,fCW_V,fMin_N]))
        mTempUVN = self.step5Matrix * mTempUVN
        vTempUVN = tObj.arrayRemove1(tObj.matrix2array(mTempUVN))

        print(' vTempUVN = ',end='')
        print(vTempUVN)

        ##################################

        ## Scale viewing volume to NDC (Step 6)
        self.step6Matrix = tObj.transformVRCtranslate(v_Dim_U,v_Dim_V,v_Dim_N)

        ##################################

        ## Combine matrices
        self.originMatrix = self.step1Matrix
        self.viewMatrix = self.step6Matrix * self.step5Matrix * self.step4Matrix * self.step3Matrix * self.step2Matrix

        wMat=np.matrix(\
            [[1,0,0,-self.wu[0]],\
             [0,1,0,-self.wv[0]],\
             [0,0,1,0],\
             [0,0,0,1]])
        sMat=np.matrix(\
            [[(self.vx[1]-self.vx[0])/(self.wu[1]-self.wu[0]),0,0,0],\
             [0,(self.vy[1]-self.vy[0])/(self.wv[1]-self.wv[0]),0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        vMat=np.matrix(\
            [[1,0,0,self.vx[0]],\
             [0,1,0,self.vy[0]],\
             [0,0,1,0],\
             [0,0,0,1]])
        tMat=np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        
        self.world2viewMatrix = vMat * sMat * wMat;

        wMat=np.matrix(\
            [[1,0,0,-self.wu[0]],\
             [0,-1,0,self.wv[1]],\
             [0,0,1,0],\
             [0,0,0,1]])
        sMat=np.matrix(\
            [[self.sx,0,0,0],\
             [0,self.sy,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])
        vMat=np.matrix(\
            [[1,0,0,self.vx[0]],\
             [0,1,0,self.vy[0]],\
             [0,0,1,0],\
             [0,0,0,1]])
        tMat=np.matrix(\
            [[1,0,0,0],\
             [0,1,0,0],\
             [0,0,1,0],\
             [0,0,0,1]])

        self.world2viewMatrix = vMat * sMat * wMat;


        self.vertices=np.matrix(self.vertices)

        ## Do not transfer from 'object space' into 'world space' until
        ## 'establish_view_matrix' called from 'load_file' in 'wood_widgets_03.py'
        self.transformed_vertices = copy.copy(self.vertices)
        
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
        self.translationMatrix = m_Trans

## Code used to test functionality
#m=mesh()
#m.set_file('/home/jeff/Dropbox/cse5365/assignments/Wood_assignment_01/pyramid_01.txt')
#m.set_file('/home/jeff/Dropbox/cse5365/assignments/Wood_assignment_01/teapot_01.txt')
#m.load()
#m.establish_matrix()
#m.establish_coordinates(500,500)


