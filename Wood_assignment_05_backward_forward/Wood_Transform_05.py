# Wood, Jeff
# 100-103-5461
# 2016-04-19
# Assignment_04

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



class Transform:
    def __init__(self):
        self.parent = self
        self.vU = []
        self.vV = []
        self.vN = []
        self.vNDCx = [-1,1]
        self.vNDCy = [-1,1]
        self.vNDCz = [0,1]
        self.vVRP = []
        self.vVPN = []
        self.vVUP = []
        self.vPRP = []
        self.perspectiveNear = None

    ##########################

    def setU(self, vU = None):
        if(vU != None):
            self.vU = vU
    def setV(self, vV = None):
        if(vV != None):
            self.vV = vV
    def setN(self, vN = None):
        if(vN != None):
            self.vN = vN
        
    def setNDCx(self, vNDCx = None):
        if(vNDCx != None):
            self.vNDCx = vNDCx
    def setNDCy(self, vNDCy = None):
        if(vNDCy != None):
            self.vNDCy = vNDCy
    def setNDCz(self, vNDCz = None):
        if(vNDCz != None):
            self.vNDCz = vNDCz
            
    def setVRP(self, vVRP = None):
        if(vVRP != None):
            self.vVRP = vVRP
    def setVPN(self, vVPN = None):
        if(vVPN != None):
            self.vVPN = vVPN
    def setVUP(self, vVUP = None):
        if(vVUP != None):
            self.vVUP = vVUP
    def setPRP(self, vPRP = None):
        if(vPRP != None):
            self.vPRP = vPRP

    ##########################

    def getU(self):
        if(self.vU):
            return self.vU
        else:
            return None
    def getV(self):
        if(self.vV):
            return self.vU
        else:
            return None
    def getN(self):
        if(self.vN):
            return self.vN
        else:
            return None
        
    def getNDCx(self):
        if(self.vNDCx):
            return self.vNDCx
        else:
            return None
    def getNDCy(self):
        if(self.vNDCy):
            return self.vNDCy
        else:
            return None
    def getNDCz(self):
        if(self.vNDCz):
            return self.vNDCz
        else:
            return None

    def getVRP(self):
        if(self.vVRP):
            return self.vVRP
        else:
            return None
    def getVPN(self):
        if(self.vVPN):
            return self.vVPN
        else:
            return None
    def getVUP(self):
        if(self.vVUP):
            return self.vVUP
        else:
            return None
    def getPRP(self):
        if(self.vPRP):
            return self.vPRP
        else:
            return None


    def setPerspectiveNear(self):
        if(self.type == 'parallel'):
            return
        vDimN = np.array(self.getN())
        vPRP = np.array(self.getPRP())
        
        ## Use vVRP' = SH*T(-vPRP)*[0 0 0 1]^T
        fFar = vDimN[1] - vPRP[2] if abs(vDimN[1] - vPRP[2]) > abs(vDimN[0] - vPRP[2]) else vDimN[0] - vPRP[2]
        fNear = vDimN[0] - vPRP[2] if abs(vDimN[1] - vPRP[2]) > abs(vDimN[0] - vPRP[2]) else vDimN[1] - vPRP[2]
#        fFar = vDimN[1] + vVRP[2] if abs(vDimN[1] + vVRP[2]) > abs(vDimN[0] + vVRP[2]) else vDimN[0] + vVRP[2] 
#        fNear = vDimN[0] + vVRP[2] if abs(vDimN[1] + vVRP[2]) > abs(vDimN[0] + vVRP[2]) else vDimN[1] + vVRP[2]
        
        self.perspectiveNear = fNear/fFar

    def getPerspectiveNear(self):
        return self.perspectiveNear
        
    ##########################

    def updateNDC(self):
        self.fNDCx = self.vNDCx[1]-self.vNDCx[0]
        self.fNDCy = self.vNDCy[1]-self.vNDCy[0]
        self.fNDCz = self.vNDCz[1]-self.vNDCz[0]
    def array2list(self,v_Array):
        return v_Array.tolist()
    def matrix2list(self,m_Matrix):
        return m_Matrix.tolist()
    def array2matrix(self,v_Array):
        vArray = np.array(v_Array)
        mReturn = np.transpose(np.matrix(vArray))
        return mReturn
    def matrix2array(self,m_Matrix):
        mMatrix = np.matrix(m_Matrix)
        vReturn = np.array(mMatrix.T)[0]
        return vReturn
    def arrayAdd1(self, v_Array):
        vArray = np.array(copy.copy(v_Array))
        vArray = np.append(vArray,1)
        return vArray
    def arrayRemove1(self, v_Array):
        vArray = np.array(copy.copy(v_Array))
        if(vArray[len(vArray)-1]==1):
            vReturn = np.delete(vArray,len(vArray)-1)
        else:
            vReturn = vArray
        return vReturn
    
    def transformVRP2Origin(self, v_VRP = None):
        comment='''
        if(v_VRP != None):
            self.setVRP(v_VRP)
        else:
            v_VRP = self.getVRP()
        '''
            
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
        
    def transformVPN2Z(self, v_VPN = None):
        comment='''
        if(v_VPN != None):
            self.setVPN(v_VPN)
        else:
            v_VPN = self.getVPN()
        '''
            
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
    
    def transformVUP2YZ(self, v_VUP = None):
        comment='''
        if(v_VUP != None):
            self.setVUP(v_VUP)
        else:
            v_VUP = self.getVUP()
        '''    
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

    def getUfromVPNandVUP(self, v_VPN = None, v_VUP = None):
        comment='''
        if(v_VPN == None):
            v_VPN = self.getVPN()

        if(v_VUP == None):
            v_VUP = self.getVUP()
        '''
        
        vVPN = np.array(v_VPN)
        vVUP = np.array(v_VUP)
        vU_nn = np.cross(vVUP,vVPN)
        vU_len = LA.norm(vU_nn)
        vU = vU_nn/vU_len
        
        return vU
    
    def getVfromVPNandU(self, v_VPN = None, v_U = None):
        comment='''
        if(v_VPN == None):
            v_VPN = self.getVPN()

        if(v_U == None):
            v_U = self.getUfromVPNandVUP(v_VPN)
        '''
            
        vVPN = np.array(v_VPN)
        vU = np.array(v_U)
        vV_nn = np.cross(vVPN,vU)
        vV_len = LA.norm(vV_nn)
        vV = vV_nn/vV_len
        
        return vV

    def getUVfromVPNandVUP(self, v_VPN = None, v_VUP = None):
        '''
        if(v_VPN == None):
            v_VPN = self.getVPN()

        if(v_VUP == None):
            v_VUP = self.getVUP()
        '''
            
        vVPN = np.array(v_VPN)
        vVUP = np.array(v_VUP)
        vU_nn = np.cross(vVUP,vVPN)
        vU_len = LA.norm(vU_nn)
        vU = vU_nn/vU_len
        vV_nn = np.cross(vVPN,vU)
        vV_len = LA.norm(vV_nn)
        vV = vV_nn/vV_len
        
        return (vU,vV)

    def transformVRCshear(self, v_PRP = None, v_Dim_U = None, v_Dim_V = None):
        comment='''
        if(v_PRP != None):
            self.setPRP(v_PRP)
        else:
            v_PRP = self.getPRP()

        if(v_Dim_U != None):
            self.setU(v_Dim_U)
        else:
            v_Dim_U = self.getU()

        if(v_Dim_V != None):
            self.setV(v_Dim_V)
        else:
            v_Dim_V = self.getV()
        '''

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

    def transformVRCtranslate_DimUVN(self, v_Dim_U = None, v_Dim_V = None, v_Dim_N = None):
        comment='''
        if(v_Dim_U != None):
            self.setU(v_Dim_U)
        else:
            v_Dim_U = self.getU()

        if(v_Dim_V != None):
            self.setV(v_Dim_V)
        else:
            v_Dim_V = self.getV()

        if(v_Dim_N != None):
            self.setN(v_Dim_N)
        else:
            v_Dim_N = self.getN()
        '''
            
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

    def transformVRCtranslate_PRP(self, v_PRP=None):
        comment='''
        if(v_PRP != None):
            self.setPRP(v_PRP)
        else:
            v_PRP = self.getPRP()
        '''

        vPRP = np.array(v_PRP)
        
        vPRP_x = vPRP[0]
        vPRP_y = vPRP[1]
        vPRP_z = vPRP[2]
        
        mReturn = np.matrix(\
            [[1, 0, 0, -vPRP_x],\
             [0, 1, 0, -vPRP_y],\
             [0, 0, 1, -vPRP_z],\
             [0, 0, 0, 1]])

        return mReturn
    
    def transformVRCscale_DimUVN(self, v_Dim_U = None, v_Dim_V = None, v_Dim_N = None):
        comment='''
        if(v_Dim_U != None):
            self.setU(v_Dim_U)
        else:
            v_Dim_U = self.getU()

        if(v_Dim_V != None):
            self.setV(v_Dim_V)
        else:
            v_Dim_V = self.getV()

        if(v_Dim_N != None):
            self.setN(v_Dim_N)
        else:
            v_Dim_N = self.getN()
        '''
            
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

    def transformVRCscale_DimUVN_VRPz(self, v_Dim_U = None, v_Dim_V = None, v_Dim_N = None, v_VRP = None):
        comment='''
        if(v_Dim_U != None):
            self.setU(v_Dim_U)
        else:
            v_Dim_U = self.getU()

        if(v_Dim_V != None):
            self.setV(v_Dim_V)
        else:
            v_Dim_V = self.getV()

        if(v_Dim_N != None):
            self.setN(v_Dim_N)
        else:
            v_Dim_N = self.getN()
        '''
            
        vDim_U = np.array(v_Dim_U)
        vDim_V = np.array(v_Dim_V)
        vDim_N = np.array(v_Dim_N)
        vVRP = np.array(v_VRP)

        fFar = vDim_N[1] + vVRP[2] if abs(vDim_N[1] + vVRP[2]) > abs(vDim_N[0] + vVRP[2]) else vDim_N[0] + vVRP[2] 
        fNear = vDim_N[0] + vVRP[2] if abs(vDim_N[1] + vVRP[2]) > abs(vDim_N[0] + vVRP[2]) else vDim_N[1] + vVRP[2]
        
        fScale_U = -2*vVRP[2]/(vDim_U[1]-vDim_U[0])
        fScale_V = -2*vVRP[2]/(vDim_V[1]-vDim_V[0])
        fScale_N = 1
        
        mUniformSlope = np.matrix(\
            [[fScale_U, 0, 0, 0],\
             [0, fScale_V, 0, 0],\
             [0, 0, fScale_N, 0],\
             [0, 0, 0, 1]])

        fScale_All = 1/fFar

        mUniformScale = np.matrix(\
            [[fScale_All, 0, 0, 0],\
             [0, fScale_All, 0, 0],\
             [0, 0, fScale_All, 0],\
             [0, 0, 0, 1]])
        
        mReturn = mUniformScale * mUniformSlope

        return mReturn

    def transformFrustum(self, v_Dim_N=None, v_PRP=None):
        if(self.type == 'parallel'):
            return
        if(v_Dim_N == None):
            v_Dim_N = self.getN()
        if(v_PRP == None):
            v_PRP = self.getVRP()
            
        vDimN = np.array(v_Dim_N)
        vPRP = np.array(v_PRP)
        ## Use vVRP' = SH*T(-vPRP)*[0 0 0 1]^T
        fFar = vDimN[1] - vPRP[2] if abs(vDimN[1] - vPRP[2]) > abs(vDimN[0] - vPRP[2]) else vDimN[0] - vPRP[2]
        fNear = vDimN[0] - vPRP[2] if abs(vDimN[1] - vPRP[2]) > abs(vDimN[0] - vPRP[2]) else vDimN[1] - vPRP[2]
#        fFar = vDimN[1] + vVRP[2] if abs(vDimN[1] + vVRP[2]) > abs(vDimN[0] + vVRP[2]) else vDimN[0] + vVRP[2] 
#        fNear = vDimN[0] + vVRP[2] if abs(vDimN[1] + vVRP[2]) > abs(vDimN[0] + vVRP[2]) else vDimN[1] + vVRP[2]
        fPerspectiveNear = fNear/fFar
        fOnePlus = 1 + fPerspectiveNear
        fOneLess = 1 - fPerspectiveNear
        
        mReturn = np.matrix([[1,0,0,0],\
                             [0,1,0,0],\
                             [0,0,1/fOneLess,-fPerspectiveNear/fOneLess],\
                             [0,0,1,0]])

        return mReturn
