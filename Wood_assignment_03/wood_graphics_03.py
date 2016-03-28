# Wood, Jeff
# 100-103-5461
# 2016-04-08
# Assignment_03

#   From:
#       http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_polygon.html
#       http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_line.html
#       http://zetcode.com/gui/tkinter/drawing/
#       http://effbot.org/tkinterbook/canvas.htm

import numpy as np
from math import *
from tkinter import *
from copy import *

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
        self.polygons=[]                                # Array storing Triangles and Quads
        self.borders=[]                                 # Array storing Viewport Box
        self.edges=[]

        canvas.delete('all')                            # Clear screen of all objects
        if(not len(mesh.transformed_vertices)):         # If no objects do not attempt to draw.
            return

        # Establish proper coordinates based on window size
        mesh.establish_coordinates(canvas.cget("width"),canvas.cget("height"))


        # DRAW viewport box
        for i in range(0,len(mesh.box)-1):
            self.borders.append(canvas.create_line(int(mesh.box[i,0]), int(mesh.box[i,1]), \
                                                   int(mesh.box[i+1,0]), int(mesh.box[i+1,1]), \
                                                   fill="black", width=1.0))

        ## DRAW all faces
        for f in range(0,len(mesh.faces)):

            v_polygon=[]
            i_indices=[]

            ## For each face loop over all indices to build
            ## [[x0,y0],[x1,y1],[x2,y2],..[xn,yn]] array
            for i in range(0,len(mesh.faces[f])):
                i_index= mesh.faces[f][i]
                i_indices.append(i_index)
                v_to_add = mesh.coordinates[i_index,:]
                
                v_polygon.append(int(v_to_add[0,0]))
                v_polygon.append(int(v_to_add[0,1]))

            ## DRAW actual faces
            self.polygons.append(canvas.create_polygon(list(v_polygon), fill='red', width=1.0, outline='black'))


    def redisplay(self,canvas,event):
        mesh=self.mesh
        print(' Redisplay called ')

        if(not len(mesh.transformed_vertices)):         # If no objects do not attempt to draw.
            return
        
        # If there are drawn objects
        if(self.borders or self.polygons):
            # RE-Establish proper coordinates based on window size
            mesh.establish_coordinates(canvas.cget("width"),canvas.cget("height"))
            
        # REPOSITION viewport box object
        if self.borders:
            for i in range(0,len(mesh.box)-1):
                canvas.coords(\
                    self.borders[i],\
                    int(mesh.box[i,0]), int(mesh.box[i,1]),\
                    int(mesh.box[i+1,0]), int(mesh.box[i+1,1])\
                )

        if self.polygons:

            ## REPOSITION all faces
            for f in range(0,len(mesh.faces)):

                v_polygon=[]
                i_indices=[]

                ## For each face loop over all indices to build
                ## [[x0,y0],[x1,y1],[x2,y2],..[xn,yn]] array
                for i in range(0,len(mesh.faces[f])):
                    i_index= mesh.faces[f][i]
                    i_indices.append(i_index)
                    v_to_add = mesh.coordinates[i_index,:]

                    v_polygon.append(v_to_add[0,0])
                    v_polygon.append(v_to_add[0,1])

                ## REPOSITION actual faces
                canvas.coords(self.polygons[f], v_polygon)
            canvas.update()

    def clear(self,canvas,event):
        mesh=self.mesh
        print(' Clear called ')
            
        # DELETE viewport box object
        if self.borders:
            for i in range(0,len(self.borders)):
                canvas.delete(self.borders[i])

        if self.polygons:

            ## DELETE all polygons
            for i in range(0,len(self.polygons)):
                canvas.delete(self.polygons[i])
                
        canvas.update()


