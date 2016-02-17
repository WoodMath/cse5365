# Wood, Jeff
# 100-103-5461
# 2016-02-17
# Assignment_01

#   From:
#       http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_polygon.html
#       http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_line.html
#       http://zetcode.com/gui/tkinter/drawing/
#       http://effbot.org/tkinterbook/canvas.htm

from numpy import *
from math import *
from tkinter import *

class cl_world:
    def __init__(self, mesh, objects=[],canvases=[],polygons=[],borders=[],edges=[]):
        self.objects=objects
        self.canvases=canvases
        self.polygons=polygons
        self.borders=borders
        self.edges=edges
        self.mesh=mesh
        
 
    def add_canvas(self,canvas):
        self.canvases.append(canvas)
        canvas.world=self
    
    def create_graphic_objects(self,canvas,mesh):
        self.polygons=[]            # Array storing Triangles and Quads
        self.borders=[]             # Array storing Viewport Box
        self.edges=[]
        
        canvas.delete('all')        # Clear screen of all objects

        # Establish matrix for window size
        mesh.establish_coordinates(canvas.cget("width"),canvas.cget("height"))


        # Draw viewport box
        for i in range(0,len(mesh.box)-1):
            self.borders.append(canvas.create_line(int(mesh.box[i,0]), int(mesh.box[i,1]), \
                                                   int(mesh.box[i+1,0]), int(mesh.box[i+1,1]), \
                                                   fill="black", width=1.0))
        
        for i in range(0,len(mesh.faces)):
            ##################################
            ## if Face containse 3 vertices ##
            ##################################
            if(len(mesh.faces[i])==3):
                ## Index of 3-corners of face
                i0=mesh.faces[i][0]
                i1=mesh.faces[i][1]
                i2=mesh.faces[i][2]
                ## Get vertex for each index
                v0=mesh.coordinates[i0,:]
                v1=mesh.coordinates[i1,:]
                v2=mesh.coordinates[i2,:]
                self.polygons.append(canvas.create_polygon(int(v0[0,0]), int(v0[0,1]), \
                                                            int(v1[0,0]), int(v1[0,1]), \
                                                            int(v2[0,0]), int(v2[0,1]), \
                                                            fill='red', width=1.0, outline='black'))
            ##################################
            ## if Face containse 4 vertices ##
            ##################################
            if(len(mesh.faces[i])==4):
                ## Index of 3-corners of face
                i0=mesh.faces[i][0]
                i1=mesh.faces[i][1]
                i2=mesh.faces[i][2]
                i3=mesh.faces[i][3]
                ## Get vertex for each index
                v0=mesh.coordinates[i0,:]
                v1=mesh.coordinates[i1,:]
                v2=mesh.coordinates[i2,:]
                v3=mesh.coordinates[i3,:]                
                self.polygons.append(canvas.create_polygon(int(v0[0,0]), int(v0[0,1]), \
                                                            int(v1[0,0]), int(v1[0,1]), \
                                                            int(v2[0,0]), int(v2[0,1]), \
                                                            int(v3[0,0]), int(v3[0,1]), \
                                                            fill='red', width=1.0, outline='black'))




    def redisplay(self,canvas,event):

        mesh=self.mesh
        if self.borders:
            mesh.establish_coordinates(canvas.cget("width"),canvas.cget("height"))
            for i in range(0,len(mesh.box)-1):
                canvas.coords(\
                    self.borders[i],\
                    int(mesh.box[i,0]), int(mesh.box[i,1]),\
                    int(mesh.box[i+1,0]), int(mesh.box[i+1,1])\
                )

        if self.polygons:
            for i in range(0,len(mesh.faces)):
                ##################################
                ## if Face containse 3 vertices ##
                ##################################    
                if(len(mesh.faces[i])==3):
                    ## Index of 3-corners of face
                    i0=mesh.faces[i][0]
                    i1=mesh.faces[i][1]
                    i2=mesh.faces[i][2]
                    ## Get vertex for each index
                    v0=mesh.coordinates[i0,:]
                    v1=mesh.coordinates[i1,:]
                    v2=mesh.coordinates[i2,:]
                    canvas.coords(\
                        self.polygons[i],\
                        int(v0[0,0]), int(v0[0,1]), \
                        int(v1[0,0]), int(v1[0,1]), \
                        int(v2[0,0]), int(v2[0,1]))
                ##################################    
                ## if Face containse 4 vertices ##
                ##################################                    
                if(len(mesh.faces[i])==4):
                    ## Index of 4-corners of face
                    i0=mesh.faces[i][0]
                    i1=mesh.faces[i][1]
                    i2=mesh.faces[i][2]
                    i3=mesh.faces[i][3]                    
                    ## Get vertex for each index
                    v0=mesh.coordinates[i0,:]
                    v1=mesh.coordinates[i1,:]
                    v2=mesh.coordinates[i2,:]
                    v3=mesh.coordinates[i3,:]                    
                    canvas.coords(\
                        self.polygons[i],\
                        int(v0[0,0]), int(v0[0,1]), \
                        int(v1[0,0]), int(v1[0,1]), \
                        int(v2[0,0]), int(v2[0,1]), \
                        int(v3[0,0]), int(v3[0,1])) 


