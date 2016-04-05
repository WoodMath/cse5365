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
from wood_transform_03 import *

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
        self.filename=[]
        self.init()
    def init(self):
        self.vertices=[]                    ## Raw vertex data (including trailing ones) from input
        self.object_coordinates=[]          ## Same as above (but copied)
        self.world_coordinates=[]           ## Coordinates after applying transformations to object
        self.view_coordinates=[]            ## Coordinates after 7-step process
        self.screen_coordinates=[]          ## Coordinates after Window Resize
        self.ndc_coordinates=[]
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
        self.viewMatrix=[]
        self.originMatrix=[]
        self.object2worldMatrix=[]
        self.world2NDCMatrix=[]
        self.object2NDCMatrix=[]
        self.NDC2viewportMatrix=[]
        self.world2viewportMatrix=[]
        self.viewport2screenMatrix=[]
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
        self.eyeMatrix=np.matrix(\
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
        self.flyMatrix=None
        self.start_index=[]
        self.group_count=[]
        self.something2draw=False


    def add_optimal_line(self,v_to_add):
        ## Performs a prefix sort / radix sort
        ## Cycles through an array of 2 element arrays such to insert an array [x,y] such that
        ##      All elements x are no less than the elements x before it.
        ##      For any given x, all elements y are no less than the elements y before it
        ##      Think [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]

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
                    v_test = self.faces[i_inc]
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
            i_ins = len(self.faces)                         ## Set insert position as end of vertice list
            self.start_index.append(i_ins)                  ## Set the start to this position
            self.group_count.append(0)                      ## Still keeping group size as 0 because element hasn't been appendied to vertice list yet

        ## Found position to insert
        i_current_vert_group_count = len(self.start_index)  ## Restablish group count

        ## Now do insert
        if(i_ins > -1):
            self.faces.insert(i_ins,v_to_add)               ## Insert actual vertex
            (self.group_count[i_current_vert_group]) += 1   ## Increase the group size by 1

            for i_inc in range(i_current_vert_group+1, i_current_vert_group_count):
                (self.start_index[i_inc]) += 1              ## Increment starting index of remaining group



    def seperate_points(self):
        v_vertices = copy.copy(self.vertices)
        v_indices = copy.copy(self.faces)
        v_out_vertices=[]
        v_out_indices=[]
        i_index = 0
        for i_inc in range(0,len(v_indices)):
            i_index_one = v_indices[i_inc][0]
            i_index_two = v_indices[i_inc][1]
            v_vertex_one = v_vertices[i_index_one]
            v_vertex_two = v_vertices[i_index_two]
            
            v_out_vertices.append(v_vertex_one)
            v_out_vertices.append(v_vertex_two)

            v_out_indices.append([i_index,i_index+1])
            i_index += 2

        self.vertices = v_out_vertices
        self.faces = v_out_indices
        
#        return (v_out_vertices,v_out_indices)

    def set_file(self,filename):
        self.filename=filename


    def add_vertex(self,vertex):
        self.vertices.append(vertex)
    def add_face(self,face):
        ## Takes a line(face) , appends 1 (as draw indicator)
        if(len(face)>2):
            raise ValueError(' Length of Passed face does not equal 2')
        if(face[0]<face[1]):
            line_to_append  = [face[0],face[1],1]
        else:
            line_to_append  = [face[1],face[0],1]

        self.add_optimal_line(line_to_append)

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
                        line_parsed=vect_float(line_parsed[:])
                        self.add_vertex(line_parsed)
                    if(line_type=='f'):
                        line_parsed = vect_int_less_one(line_parsed[:])
                        for k in range(len(line_parsed)-1):
                            line_passed = [line_parsed[k],line_parsed[k+1]]
                            self.add_face(line_passed)
                        ## Add line back to beginning
                        if(len(line_parsed)>2):
                            if(line_parsed[0] != line_parsed[len(line_parsed)-1]):      ## Some formats repeat 1st vertex
                                line_passed = [line_parsed[0], line_parsed[len(line_parsed)-1]]
                                self.add_face(line_passed)
                        #self.add_face(line_parsed)
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
        self.seperate_points()
        self.object_coordinates = np.matrix(self.vertices)
        self.object2worldMatix = copy.copy(self.eyeMatrix)

#    def establish_world_matrix(self):
#        self.world_coordinates =  self.stackMatrix * np.transpose(np.matrix(self.object_coordinates))
#        self.world_coordinates = np.transpose(world_coordinates)

    def establish_NDC_coordinates(self):
        self.establish_origin_matrix()
        self.world2NDCMatrix = self.viewMatrix * self.originMatrix
        self.ndc_coordinates = self.world2NDCMatrix * self.stackMatrix * np.transpose(np.matrix(self.object_coordinates))
        self.ndc_coordinates = np.transpose(self.ndc_coordinates)

        ##################################
        ##      Clipping Occurs Here    ##
        ##################################

        
        
    def establish_screen_coordinates(self,iWidth,iHeight):

        self.viewport2screenMatrix = np.matrix(\
            [[float(iWidth),0,0,0],\
             [0,float(iHeight),0,0],\
             [0,0,1,0],\
             [0,0,0,1]])

        print(' Establishing Screen coordinates ')
        # Transform vertices into coordinates
#        self.screen_coordinates = self.viewport2screenMatrix *\
#                                  self.NDC2viewportMatrix * self.world2NDCMatrix * \
#                                  self.stackMatrix * \
#                                  np.transpose(np.matrix(self.object_coordinates))

        self.screen_coordinates = self.viewport2screenMatrix *\
                                  self.NDC2viewportMatrix * \
                                  np.transpose(np.matrix(self.ndc_coordinates))

        
        self.screen_coordinates = np.transpose(self.screen_coordinates)

        # Transform viewport box
        self.box = self.viewport2screenMatrix * np.transpose(np.matrix(self.bounding))
        self.box = np.transpose(self.box)

    def establish_view_matrix(self):
        self.establish_parallel_view_matrix()
        self.establish_NDC_coordinates()
        self.establish_viewport_matrix()

    def establish_viewport_matrix(self):
        wMat=np.matrix(\
            [[1,0,0,-self.wu[0]],\
             [0,-1,0,self.wv[1]],\
             [0,0,1,-self.wn[0]],\
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

        self.NDC2viewportMatrix = vMat * sMat * wMat;
        self.world2viewportMatrix = self.NDC2viewportMatrix * self.world2NDCMatrix

    def establish_origin_matrix(self):
        print(' Establishing origin matrix ')

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

        ## Combine matrices
        self.originMatrix = self.step1Matrix
#        self.viewMatrix = self.step6Matrix * self.step5Matrix * self.step4Matrix * self.step3Matrix * self.step2Matrix

#        self.world2NDCMatrix = self.viewMatrix * self.originMatrix

    def establish_after_origin_matrix(self):
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
#        self.originMatrix = self.step1Matrix
        self.viewMatrix = self.step6Matrix * self.step5Matrix * self.step4Matrix * self.step3Matrix * self.step2Matrix

        self.world2NDCMatrix = self.viewMatrix * self.originMatrix

    def establish_parallel_view_matrix(self):
        print(' Establishing view matrix ')

        tObj = viewTransform()

        print(' ** File Parameters ** ')

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

        self.world2NDCMatrix = self.viewMatrix * self.originMatrix
        
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
            [[1,0,0,-v_inc_fly[0]],\
             [0,1,0,-v_inc_fly[1]],\
             [0,0,1,-v_inc_fly[2]],\
             [0,0,0,1]])

        ## Rename translation matrix for consistancy
        self.flyMatrix = m_Fly

## Code used to test functionality
#m=mesh()
#m.set_file('/home/jeff/Dropbox/cse5365/assignments/Wood_assignment_01/pyramid_01.txt')
#m.set_file('/home/jeff/Dropbox/cse5365/assignments/Wood_assignment_01/teapot_01.txt')
#m.load()
#m.establish_matrix()
#m.establish_coordinates(500,500)


