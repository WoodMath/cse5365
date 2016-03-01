# Wood, Jeff
# 100-103-5461
# 2016-03-02
# Assignment_02

from tkinter import *
from math import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from wood_fileread_02 import *

import time

class cl_widgets:
    def __init__(self,ob_root_window,ob_world=[],ob_mesh=mesh()):
        self.ob_root_window=ob_root_window
        ob_root_window.title("Wood_Assignment_02")
        self.ob_world=ob_world
        self.mesh=ob_mesh
        self.pannel_03 = cl_pannel_03(self,ob_root_window,ob_mesh)
        self.ob_canvas_frame=cl_canvas_frame(self)
        self.ob_world.add_canvas(self.ob_canvas_frame.canvas)
        self.ob_canvas_frame.canvas.delete("all")


#        callback = self.ob_canvas_frame.canvas.after(5, self.ob_world.redisplay(self.ob_canvas_frame.canvas,event=None))
#        callback = self.ob_canvas_frame.canvas.after(5, self.ob_world.redisplay(self.ob_canvas_frame.canvas,event=None))
        
#        callback = self.ob_canvas_frame.canvas.after(4, self.ob_world.redisplay(self.ob_canvas_frame.canvas,event=None))


class cl_canvas_frame:
    def __init__(self, master):
        self.master=master
        self.canvas = Canvas(master.ob_root_window,width=640, height=640, bg="yellow", highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)


                                            
        self.canvas.bind('<Configure>', self.canvas_resized_callback) 
        self.canvas.bind("<ButtonPress-1>", self.left_mouse_click_callback)
        #self.canvas.bind("<ButtonRelease-1>", self.left_mouse_release_callback)
        #self.canvas.bind("<B1-Motion>", self.left_mouse_down_motion_callback)
        #self.canvas.bind("<ButtonPress-3>", self.right_mouse_click_callback)
        #self.canvas.bind("<ButtonRelease-3>", self.right_mouse_release_callback)
        #self.canvas.bind("<B3-Motion>", self.right_mouse_down_motion_callback)
        #self.canvas.bind("<Key>", self.key_pressed_callback)    
        self.canvas.bind("<Up>", self.up_arrow_pressed_callback)
        self.canvas.bind("<Down>", self.down_arrow_pressed_callback)
        self.canvas.bind("<Right>", self.right_arrow_pressed_callback)
        self.canvas.bind("<Left>", self.left_arrow_pressed_callback)     
        self.canvas.bind("<Shift-Up>", self.shift_up_arrow_pressed_callback)
        self.canvas.bind("<Shift-Down>", self.shift_down_arrow_pressed_callback)
        self.canvas.bind("<Shift-Right>", self.shift_right_arrow_pressed_callback)
        self.canvas.bind("<Shift-Left>", self.shift_left_arrow_pressed_callback)   
        self.canvas.bind("f", self.f_key_pressed_callback)  
        self.canvas.bind("b", self.b_key_pressed_callback)  
    def key_pressed_callback(self,event):
        print ('key pressed')      
    def up_arrow_pressed_callback(self,event):
        print ('pressed up')
        
    def down_arrow_pressed_callback(self,event):
        print ('pressed down')     
    def right_arrow_pressed_callback(self,event):
        print ('pressed right')       
    def left_arrow_pressed_callback(self,event):
        print ('pressed left')       
    def shift_up_arrow_pressed_callback(self,event):
        self.canvas.world.translate(0,.1,0,1)
    def shift_down_arrow_pressed_callback(self,event):
        pass
    def shift_right_arrow_pressed_callback(self,event):
        pass
    def shift_left_arrow_pressed_callback(self,event):
        pass
    def f_key_pressed_callback(self,event):

        print ("f key was pressed")
    def b_key_pressed_callback(self,event):
        
        print ("b key was pressed")         
    def left_mouse_click_callback(self,event):
        print ('Left mouse button was clicked')
        print ('x=',event.x, '   y=',event.y)
        
        
        self.x = event.x
        self.y = event.y  
        self.canvas.focus_set()
    def left_mouse_release_callback(self,event):
        print ('Left mouse button was released')
        print ('x=',event.x, '   y=',event.y)
        print ('canvas width', self.canvas.cget("width"))
        self.x = None
        self.y = None
        
    def left_mouse_down_motion_callback(self,event):
        print ('Left mouse down motion')
        print ('x=',event.x, '   y=',event.y)
        self.x = event.x
        self.y = event.y 
        
    def right_mouse_click_callback(self,event):
        
        self.x = event.x
        self.y = event.y   
    def right_mouse_release_callback(self,event):
        
        self.x = None
        self.y = None        
    def right_mouse_down_motion_callback(self,event):
        pass
    def canvas_resized_callback(self,event):
        self.canvas.config(width=event.width,height=event.height)
        
        self.canvas.pack()
        print ('canvas width', self.canvas.cget("width"))
        print ('canvas height', self.canvas.cget("height"))

        # Call redisplay() method in 'wood_graphics_02.py'
        self.master.ob_world.redisplay(self.master.ob_canvas_frame.canvas,event)

class cl_pannel_03:
    def __init__(self, master, ob_root_window, ob_mesh):
        self.master=master
        self.canvas = master.ob_root_window
        self.mesh = ob_mesh




        frame = Frame(master.ob_root_window)
        frame.pack()

        self.filename = StringVar()

        self.file_location_label = Label(frame, text="File Name:").pack(side=LEFT,padx=10,pady=10)
#        self.file_location_entry = Entry(frame, text="File Name", textvariable=self.filename, width=50).pack(side=LEFT,padx=0, pady=0)
        self.file_location_labe = Label(frame, textvariable=self.filename, width=50).pack(side=LEFT,padx=0,pady=0)

        self.file_dialog_button = Button(frame, text="Browse", fg="blue", command=self.browse_file)
        self.file_dialog_button.pack(side=LEFT)        

        self.var_filename = StringVar()
        self.var_filename.set('')
        self.button = Button(frame, text="Load", fg="red", command=self.load_file)
        self.button.pack(side=LEFT)

        axis_frame = Frame(master.ob_root_window)
        axis_frame.pack()

        self.i_rotate_option = IntVar(value=1)

        self.rotate_axis_label = Label(axis_frame, text="Rotation").pack(side=LEFT,padx=0,pady=0)
        self.rotate_axis_x = Radiobutton(axis_frame, text="X", variable=self.i_rotate_option, value=1).pack(side=LEFT,anchor=W,padx=0,pady=0)
        self.rotate_axis_y = Radiobutton(axis_frame, text="Y", variable=self.i_rotate_option, value=2).pack(side=LEFT,anchor=W,padx=0,pady=0)
        self.rotate_axis_z = Radiobutton(axis_frame, text="Z", variable=self.i_rotate_option, value=3).pack(side=LEFT,anchor=W,padx=0,pady=0)
        self.rotate_ab = Radiobutton(axis_frame, text="Line AB", variable=self.i_rotate_option, value=4).pack(side=LEFT,anchor=W,padx=0,pady=0)

        self.fDefaultZero = 0.0
        self.fDefaultOne = 1.0
        
        self.fRotateAx = self.fDefaultZero
        self.sRotateAx = StringVar(value=str(round(self.fRotateAx,2)))
        self.fRotateAy = self.fDefaultZero
        self.sRotateAy = StringVar(value=str(round(self.fRotateAy,2)))
        self.fRotateAz = self.fDefaultZero
        self.sRotateAz = StringVar(value=str(round(self.fRotateAz,2)))

        self.fRotateBx = self.fDefaultOne
        self.sRotateBx = StringVar(value=str(round(self.fRotateBx,2)))
        self.fRotateBy = self.fDefaultOne
        self.sRotateBy = StringVar(value=str(round(self.fRotateBy,2)))
        self.fRotateBz = self.fDefaultOne
        self.sRotateBz = StringVar(value=str(round(self.fRotateBz,2)))

#        self.rotate_ax.delete(0, END)
#        self.rotate_ax.insert(0, "1.0")
        
        self.rotate_a_label = Label(axis_frame, text="A:").pack(side=LEFT,padx=0,pady=0)
        self.rotate_ax = Entry(axis_frame, textvariable=self.sRotateAx, width=3).pack(side=LEFT,padx=0, pady=0)
        self.rotate_ay = Entry(axis_frame, textvariable=self.sRotateAy, width=3).pack(side=LEFT,padx=0, pady=0)
        self.rotate_az = Entry(axis_frame, textvariable=self.sRotateAz, width=3).pack(side=LEFT,padx=0, pady=0)
        
        self.rotate_b_label = Label(axis_frame, text="B:").pack(side=LEFT,padx=0,pady=0)
        self.rotate_bx = Entry(axis_frame, textvariable=self.sRotateBx, width=3).pack(side=LEFT,padx=0, pady=0)
        self.rotate_by = Entry(axis_frame, textvariable=self.sRotateBy, width=3).pack(side=LEFT,padx=0, pady=0)
        self.rotate_bz = Entry(axis_frame, textvariable=self.sRotateBz, width=3).pack(side=LEFT,padx=0, pady=0)

        self.sRotateDegrees=StringVar(value='0')
        self.rotate_degrees_label = Label(axis_frame, text="Degree:").pack(side=LEFT,padx=0,pady=0)
        self.rotate_degrees_spinbox = Spinbox(axis_frame, from_=-360, to=360, width=3, textvariable=self.sRotateDegrees)
        self.rotate_degrees_spinbox.delete(0,"end")
        self.rotate_degrees_spinbox.insert(0,"0")
        self.rotate_degrees_spinbox.pack(side=LEFT, padx=0, pady=0)

        self.sRotateSteps=StringVar(value='1')
        self.rotate_steps_label = Label(axis_frame, text="Steps:").pack(side=LEFT,padx=0,pady=0)
        self.rotate_steps_spinbox = Spinbox(axis_frame, from_=0, to=10, width=3, textvariable=self.sRotateSteps)
        self.rotate_steps_spinbox.delete(0,"end")
        self.rotate_steps_spinbox.insert(0,"1")
        self.rotate_steps_spinbox.pack(side=LEFT, padx=0, pady=0)

        self.rotate_button = Button(axis_frame, text="Rotate", fg="green", command=self.rotate)
        self.rotate_button.pack(side=LEFT)                         

        scale_frame = Frame(master.ob_root_window)
        scale_frame.pack()

        self.i_scale_option = IntVar(value=1)
        self.scale_label = Label(scale_frame, text="Scale Ratio:").pack(side=LEFT,padx=0,pady=0)
        self.scale_all = Radiobutton(scale_frame, text="All", variable=self.i_scale_option, value=1).pack(side=LEFT,anchor=W)

        self.sScaleSize=StringVar(value="1.00")
        self.scale_size_spinbox = Spinbox(scale_frame, textvariable=self.sScaleSize, values=("0.25","0.50","0.75","1.00","1.25","1.50","1.75","2.00","2.25","2.50","2.75","3.00","3.25","3.50","3.75","4.00"), width=4)
        self.scale_size_spinbox.delete(0,"end")
        self.scale_size_spinbox.insert(0,"1.00")
        self.scale_size_spinbox.pack(side=LEFT, padx=0, pady=0)

        self.scale_size_sxsysz = Radiobutton(scale_frame, text="[Sx,Sy,Sz]", variable=self.i_scale_option, value=2).pack(side=LEFT,anchor=W)

        self.fScaleSx = self.fDefaultOne
        self.sScaleSx = StringVar(value=str(round(self.fScaleSx,2)))
        self.fScaleSy = self.fDefaultOne
        self.sScaleSy = StringVar(value=str(round(self.fScaleSy,2)))
        self.fScaleSz = self.fDefaultOne
        self.sScaleSz = StringVar(value=str(round(self.fScaleSz,2)))

        self.fScaleAx = self.fDefaultZero
        self.sScaleAx = StringVar(value=str(round(self.fScaleAx,2)))
        self.fScaleAy = self.fDefaultZero
        self.sScaleAy = StringVar(value=str(round(self.fScaleAy,2)))
        self.fScaleAz = self.fDefaultZero
        self.sScaleAz = StringVar(value=str(round(self.fScaleAz,2)))
        
        self.scale_sx = Entry(scale_frame, textvariable=self.sScaleSx, width=3).pack(side=LEFT,padx=0, pady=0)
        self.scale_sy = Entry(scale_frame, textvariable=self.sScaleSy, width=3).pack(side=LEFT,padx=0, pady=0)
        self.scale_sz = Entry(scale_frame, textvariable=self.sScaleSz, width=3).pack(side=LEFT,padx=0, pady=0)

        self.scale_a_label = Label(scale_frame, text="Center of Scale:").pack(side=LEFT,padx=0,pady=0)

        self.scale_ax = Entry(scale_frame, textvariable=self.sScaleAx, width=3).pack(side=LEFT,padx=0, pady=0)
        self.scale_ay = Entry(scale_frame, textvariable=self.sScaleAy, width=3).pack(side=LEFT,padx=0, pady=0)
        self.scale_az = Entry(scale_frame, textvariable=self.sScaleAz, width=3).pack(side=LEFT,padx=0, pady=0)

        self.sScaleSteps=StringVar(value='1')
        self.scale_steps_label = Label(scale_frame, text="Steps:").pack(side=LEFT,padx=0,pady=0)
        self.scale_steps_spinbox = Spinbox(scale_frame, from_=0, to=10, width=3, textvariable=self.sScaleSteps)
        self.scale_steps_spinbox.delete(0,"end")
        self.scale_steps_spinbox.insert(0,"1")
        self.scale_steps_spinbox.pack(side=LEFT, padx=0, pady=0)

        self.scale_button = Button(scale_frame, text="Scale", fg="green", command=self.scale)
        self.scale_button.pack(side=LEFT)

#        disc_frame_one = Frame(master.ob_root_window)
#        disc_frame_one.pack()
#        self.disc_label_one = Label(disc_frame_one, text="NOTE: Transformations are cumulative").pack(side=LEFT,padx=0,pady=0)

#        disc_frame_two = Frame(master.ob_root_window)
#        disc_frame_two.pack()
#        self.disc_label_two = Label(disc_frame_two, text="Click 'Draw' to reset transformation stack.").pack(side=LEFT,padx=0,pady=0)

        disc_frame_thr = Frame(master.ob_root_window)
        disc_frame_thr.pack()
        self.disc_label_thr = Label(disc_frame_thr, text="NOTE: Transformations are cumulative. Click 'Load' to reset transformation stack.")
        self.disc_label_thr.pack(side=LEFT,padx=0,pady=0)

        
    def browse_file(self):
        self.var_filename.set(filedialog.askopenfilename(filetypes=[("allfiles","*"),("pythonfiles","*.txt")]))
        filename = self.var_filename.get()

        # Save filename to 'mesh' object
        self.mesh.filename=filename
        
        self.filename.set(filename)        
        
        print(" Loading file '" + str(filename) + "'")
        if(len(self.mesh.filename)):
            self.mesh.set_file(self.mesh.filename)
            self.mesh.load()
            

    def load_file(self):
        if(not len(self.mesh.vertices)):  # If no objects do not attempt to transform.
            return
        else:
            
            # Calculate non-canvas size matrix transformations
            self.mesh.establish_matrices()
            print('window:')
            print(' wxmin = ' + str(self.mesh.wx[0]))
            print(' wxmax = ' + str(self.mesh.wx[1]))        
            print(' wymin = ' + str(self.mesh.wy[0]))
            print(' wymax = ' + str(self.mesh.wy[1]))        
            print(' ')
            print('viewport:')
            print(' vxmin = ' + str(self.mesh.vx[0]))
            print(' vxmax = ' + str(self.mesh.vx[1]))        
            print(' vymin = ' + str(self.mesh.vy[0]))
            print(' vymax = ' + str(self.mesh.vy[1])) 
            print(' ')

            # Call create_graphic_objects() method in 'wood_graphics_02.py'
            self.master.ob_world.create_graphic_objects(self.master.ob_canvas_frame.canvas,self.mesh)

            print ( "called the draw callback!")

    def rotate_callback(self,i_iteration):
        
        if(i_iteration):
            self.mesh.establish_rotation_matrices(self.rotate_steps, self.v_a, self.v_b, self.rotate_degrees)
            # Call redisplay() method in 'wood_graphics_02.py'
            self.master.ob_world.redisplay(self.master.ob_canvas_frame.canvas,event=None)
            # self.master.ob_canvas_frame.canvas.update()
            self.master.ob_root_window.after(50, self.rotate_callback(i_iteration-1))
        else:
            return
            
    def rotate(self):
        print(' rotate button pushed ')

        if(not len(self.mesh.transformed_vertices)):  # If no objects do not attempt to transform.
            return

        self.v_a = [0.0,0.0,0.0]

        self.rotate_option = self.i_rotate_option.get()

        # If X-axis selected
        if(self.rotate_option==1):
            self.v_b = [1.0,0.0,0.0]
        # If Y-axis selected
        elif(self.rotate_option==2):
            self.v_b = [0.0,1.0,0.0]
        # If Z-axis selected
        elif(self.rotate_option==3):
            self.v_b = [0.0,0.0,1.0]
        # Else assign axis based on vector 'ab'
        else:
            self.fRotateAx = float(self.sRotateAx.get())
            self.fRotateAy = float(self.sRotateAy.get())
            self.fRotateAz = float(self.sRotateAz.get())

            self.fRotateBx = float(self.sRotateBx.get())
            self.fRotateBy = float(self.sRotateBy.get())
            self.fRotateBz = float(self.sRotateBz.get())

            self.v_a = [self.fRotateAx, self.fRotateAy, self.fRotateAz]
            self.v_b = [self.fRotateBx, self.fRotateBy, self.fRotateBz]
            

        self.rotate_degrees = int(self.sRotateDegrees.get())
        self.rotate_steps = int(self.sRotateSteps.get())

        if(self.rotate_steps<1):
            self.rotate_steps=1

        print(' self.rotate_option = ' + str(self.rotate_option))
        print(' self.v_a = ' + str(self.v_a))
        print(' self.v_b = ' + str(self.v_b))
        print(' self.rotate_degrees = ' + str(self.rotate_degrees))
        print(' self.rotate_steps = ' + str(self.rotate_steps))

        # Iterative callback used for animation and redisplay
        self.master.ob_root_window.after(0, self.rotate_callback(self.rotate_steps))

    def scale_callback(self,i_iteration):
        if(i_iteration):
            print(' self.scale_steps = ' + str(self.scale_steps))
            self.mesh.establish_scale_matrices(self.scale_steps, self.scale_size, self.scale_center)
            # Call redisplay() method in 'wood_graphics_02.py'
            self.master.ob_world.redisplay(self.master.ob_canvas_frame.canvas,event=None)
            # self.master.ob_canvas_frame.canvas.update()
            self.master.ob_root_window.after(50, self.scale_callback(i_iteration-1))
        else:
            return

    def scale(self):
        print(' scale button clicked ')

        if(not len(self.mesh.transformed_vertices)):  # If no objects do not attempt to transform.
            return
        
        self.scale_option = self.i_scale_option.get()

        self.scale_uniform_size = float(self.sScaleSize.get())

        self.fScaleSx = float(self.sScaleSx.get())
        self.fScaleSy = float(self.sScaleSy.get())
        self.fScaleSz = float(self.sScaleSz.get())

        self.fScaleAx = float(self.sScaleAx.get())
        self.fScaleAy = float(self.sScaleAy.get())
        self.fScaleAz = float(self.sScaleAz.get())

        self.scale_center = [self.fScaleAx, self.fScaleAy, self.fScaleAz]
        self.scale_size = [1.0,1.0,1.0]

        # If uniform scale selected assign same scale to all array elements
        if(self.scale_option==1):
            self.scale_size = [self.scale_uniform_size, self.scale_uniform_size, self.scale_uniform_size]
        # Else assign differing scale to array based on dimension
        else:
            self.scale_size = [self.fScaleSx, self.fScaleSy, self.fScaleSz]

        self.scale_steps = int(self.sScaleSteps.get())
        if(self.scale_steps<1):
            self.scale_steps=1
            
        print(' self.scale_option = ' + str(self.scale_option))
        print(' self.scale_uniform_size = ' + str(self.scale_uniform_size))
        print(' self.scale_size = ' + str(self.scale_size))
        print(' self.scale_center = ' + str(self.scale_center))
        print(' self.scale_steps = ' + str(self.scale_steps))

        # Iterative callback used for animation and redisplay
        self.master.ob_root_window.after(0, self.scale_callback(self.scale_steps))
            


class MyDialog(simpledialog.Dialog):
    def body(self, master):

        Label(master, text="Integer:").grid(row=0, sticky=W)
        Label(master, text="Float:").grid(row=1, column=0 ,sticky=W)
        Label(master, text="String:").grid(row=1, column=2 , sticky=W)
        self.e1 = Entry(master)
        self.e1.insert(0, 0)
        self.e2 = Entry(master)
        self.e2.insert(0, 4.2)
        self.e3 = Entry(master)
        self.e3.insert(0, 'Default text')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=1, column=3)
        
        
        self.cb = Checkbutton(master, text="Hardcopy")
        self.cb.grid(row=3, columnspan=2, sticky=W)


    def apply(self):
        try:
            first = int(self.e1.get())
            second = float(self.e2.get())
            third=self.e3.get()
            self.result = first, second, third
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input",
                "Illegal values, please try again"
            )

class cl_statusBar_frame:
    def __init__(self, master):
        self.master=master
        status = StatusBar(master.ob_root_window)
        status.pack(side=BOTTOM, fill=X)
        status.set('%s','This is the status bar')

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
        
class cl_toolbar:
    def __init__(self, master):
        self.master=master
        self.toolbar = Frame(master.ob_root_window)
        self.button = Button(self.toolbar, text="Draw", width=16, command=self.toolbar_draw_callback)
        self.button.pack(side=LEFT, padx=2, pady=2)

        self.button = Button(self.toolbar, text="Toolbar Button 2", width=16, command=self.toolbar_callback)
        self.button.pack(side=RIGHT, padx=2, pady=2)

        self.toolbar.pack(side=TOP, fill=X)
    def toolbar_draw_callback(self):
        self.master.ob_world.create_graphic_objects(self.master.ob_canvas_frame.canvas)
        print ( "called the draw callback!")
    
    def toolbar_callback(self):
        print ( "called the toolbar callback!")

