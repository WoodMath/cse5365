# Wood, Jeff
# 100-103-5461
# 2016-04-19
# Assignment_04

from numpy  import *
from math import *
from tkinter import *


class cl_world:
    def __init__(self, objects=[],canvases=[]):
        self.objects=objects
        self.canvases=canvases
        self.controller = None        
 
    def add_canvas(self,canvas):
        self.canvases.append(canvas)
        canvas.world=self

    def create_graphic_objects(self):
        return
    def redisplay_graphic_objects(self):
        self.controller.updateResize()
        return
    def old_create_graphic_objects(self,canvas):
        self.objects.append(canvas.create_line(0,0,canvas.cget("width"),canvas.cget("height")))
        self.objects.append(canvas.create_line(canvas.cget("width"),0,0,canvas.cget("height")))
        self.objects.append(canvas.create_oval(int(0.25*int(canvas.cget("width"))),
            int(0.25*int(canvas.cget("height"))),
            int(0.75*int(canvas.cget("width"))),
            int(0.75*int(canvas.cget("height")))))        
    
    def old_redisplay(self,canvas,event):
        if self.objects:
           canvas.coords(self.objects[0],0,0,event.width,event.height)
           canvas.coords(self.objects[1],event.width,0,0,event.height)
           canvas.coords(self.objects[2],int(0.25*int(event.width)),
               int(0.25*int(event.height)),
               int(0.75*int(event.width)),
               int(0.75*int(event.height)))        
