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
    def __init__(self, mesh, objects=[],canvases=[],lines=[],borders=[],edges=[]):
        self.objects=objects
        self.canvases=canvases
        self.lines=lines
        self.borders=borders
        self.edges=edges
        self.mesh=mesh
        self.canvas=None
        
 
    def add_canvas(self,canvas):
        self.canvases.append(canvas)
        canvas.world=self
    
    def create_graphic_objects(self,canvas,mesh):
        self.lines=[]                                # Array storing Triangles and Quads
        self.borders=[]                                 # Array storing Viewport Box
        self.edges=[]
        
        canvas.delete('all')                            # Clear screen of all objects
        if(not len(mesh.vertices) and not (mesh.something2draw)):         # If no objects do not attempt to draw.
            return

        # Establish proper coordinates based on window size
#        mesh.establish_screen_coordinates(canvas.cget("width"),canvas.cget("height"))


        # DRAW viewport box
        for i in range(0,len(mesh.box)-1):
            self.borders.append(canvas.create_line(int(mesh.box[i,0]), int(mesh.box[i,1]), \
                                                   int(mesh.box[i+1,0]), int(mesh.box[i+1,1]), \
                                                   fill="black", width=1.0))
        
        ## DRAW all faces
        for f in range(0,len(mesh.faces)):

            v_line=[]
            i_one = mesh.faces[f][0]
            i_two = mesh.faces[f][1]
            v_to_add_one = mesh.screen_coordinates[i_one,:]
            v_to_add_two = mesh.screen_coordinates[i_two,:]
#            v_line.append(int(v_to_add_one[0,0]))
#            v_line.append(int(v_to_add_one[0,1]))
#            v_line.append(int(v_to_add_two[0,0]))
#            v_line.append(int(v_to_add_two[0,1]))
            v_line = [v_to_add_one[0,0],v_to_add_one[0,1],v_to_add_two[0,0],v_to_add_two[0,1]]

            ## For each face loop over all indices to build
            ## [[x0,y0],[x1,y1],[x2,y2],..[xn,yn]] array
#            for i in range(0,len(mesh.faces[f])):
#                i_index= mesh.faces[f][i]

#                i_indices.append(i_index)

#                v_to_add = mesh.screen_coordinates[i_index,:]
                
#                v_line.append(int(v_to_add[0,0]))
#                v_line.append(int(v_to_add[0,1]))


            ## DRAW actual faces
#            self.lines.append(canvas.create_polygon(list(v_line), fill='red', width=1.0, outline='black'))
            ## DRAW actual lines
            self.lines.append(canvas.create_line(v_line, width=1.0, fill='black'))


    def redisplay(self,canvas,event):
        mesh=self.mesh
        print(' Redisplay called ')

        if(not len(mesh.vertices) and (not mesh.something2draw)):         # If no objects do not attempt to draw.
            return
        
#        # If there are drawn objects
#        if(self.borders or self.lines):
#            # RE-Establish proper coordinates based on window size
#            mesh.establish_screen_coordinates(canvas.cget("width"),canvas.cget("height"))
            
        # REPOSITION viewport box object
        if self.borders:
            for i in range(0,len(mesh.box)-1):
                canvas.coords(\
                    self.borders[i],\
                    int(mesh.box[i,0]), int(mesh.box[i,1]),\
                    int(mesh.box[i+1,0]), int(mesh.box[i+1,1])\
                )

        if self.lines:
            ## REPOSITION all faces
            for f in range(0,len(mesh.faces)):
                v_line=[]
                i_indices=[]

                i_one = mesh.faces[f][0]
                i_two = mesh.faces[f][1]
                v_to_add_one = mesh.screen_coordinates[i_one,:]
                v_to_add_two = mesh.screen_coordinates[i_two,:]
                v_line = [v_to_add_one[0,0],v_to_add_one[0,1],v_to_add_two[0,0],v_to_add_two[0,1]]
                canvas.coords(self.lines[f], v_line)

#                ## For each face loop over all indices to build
#                ## [[x0,y0],[x1,y1],[x2,y2],..[xn,yn]] array
#                for i in range(0,len(mesh.faces[f])):
#                    i_index= mesh.faces[f][i]
#                    i_indices.append(i_index)
#                    v_to_add = mesh.screen_coordinates[i_index,:]
#
#                    v_line.append(v_to_add[0,0])
#                    v_line.append(v_to_add[0,1])
#
#                ## REPOSITION actual faces
#                canvas.coords(self.lines[f], v_line)
            canvas.update()

    def clear(self,canvas,event=None):
        mesh=self.mesh
        print(' Clear called ')

        canvas.delete('all')
        canvas.delete(ALL)
        
        # DELETE viewport box object
        if self.borders:
            for i in range(0,len(self.borders)):
                self.borders[i]
                canvas.delete(self.borders[i])

        if self.lines:

            ## DELETE all lines
            for i in range(0,len(self.lines)):
                j=self.lines[i]
                k=canvas.delete(self.lines[i])

        self.borders=[]
        self.lines=[]
        #canvas.update()


