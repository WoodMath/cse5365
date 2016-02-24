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
from tkValidatingEntry import *

class cl_widgets:
    def __init__(self,ob_root_window,ob_world=[],ob_mesh=mesh()):
        self.ob_root_window=ob_root_window
        ob_root_window.title("Wood_Assignment_02")
        self.ob_world=ob_world
        self.mesh=ob_mesh
        self.pannel_03 = cl_pannel_03(self,ob_mesh)
        self.ob_canvas_frame=cl_canvas_frame(self)
        self.ob_world.add_canvas(self.ob_canvas_frame.canvas)
        self.ob_canvas_frame.canvas.delete("all")


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

        # Call redisplay() method in 'wood_graphics_01.py'
        self.master.ob_world.redisplay(self.master.ob_canvas_frame.canvas,event)

class cl_pannel_03:
    def __init__(self, master,ob_mesh):
        self.master=master
        self.canvas = master.ob_root_window
        self.mesh = ob_mesh

        frame = Frame(master.ob_root_window)
        frame.pack()

        self.file_location_label = Label(frame, text="File Name").pack(side=LEFT,padx=10,pady=10)
        self.file_location_entry = Entry(frame, width=50).pack(side=LEFT,padx=10, pady=10)

        self.file_dialog_button = Button(frame, text="Open File Dialog", fg="blue", command=self.browse_file)
        self.file_dialog_button.pack(side=LEFT)        

        self.var_filename = StringVar()
        self.var_filename.set('')
        self.button = Button(frame, text="Load File (Draw)", fg="red", command=self.load_file)
        self.button.pack(side=LEFT)

        axis_frame = Frame(master.ob_root_window)
        axis_frame.pack()

        i_axis = IntVar(value=1)

        self.axis_label = Label(axis_frame, text="Rotation").pack(side=LEFT,padx=10,pady=0)
        self.axis_x = Radiobutton(axis_frame, text="X", variable=i_axis, value=1).pack(side=LEFT,anchor=W)
        self.axis_y = Radiobutton(axis_frame, text="Y", variable=i_axis, value=2).pack(side=LEFT,anchor=W)
        self.axis_z = Radiobutton(axis_frame, text="Z", variable=i_axis, value=3).pack(side=LEFT,anchor=W)
        self.rotate_ab = Radiobutton(axis_frame, text="Line AB", variable=i_axis, value=4).pack(side=LEFT,anchor=W, padx=10)

        fDefaultZero = 0.0
        fDefaultOne = 1.0
        
        fRotateAx = fDefaultZero
        sRotateAx = StringVar(value=str(round(fRotateAx,2)))
        fRotateAy = fDefaultZero
        sRotateAy = StringVar(value=str(round(fRotateAy,2)))
        fRotateAz = fDefaultZero
        sRotateAz = StringVar(value=str(round(fRotateAz,2)))

        fRotateBx = fDefaultOne
        sRotateBx = StringVar(value=str(round(fRotateBx,2)))
        fRotateBy = fDefaultOne
        sRotateBy = StringVar(value=str(round(fRotateBy,2)))
        fRotateBz = fDefaultOne
        sRotateBz = StringVar(value=str(round(fRotateBz,2)))

#        self.rotate_ax.delete(0, END)
#        self.rotate_ax.insert(0, "1.0")
        
        self.rotate_a_label = Label(axis_frame, text="A:").pack(side=LEFT,padx=0,pady=0)
        self.rotate_ax = Entry(axis_frame, textvariable=sRotateAx, width=3).pack(side=LEFT,padx=0, pady=0)
        self.rotate_ay = Entry(axis_frame, textvariable=sRotateAy, width=3).pack(side=LEFT,padx=0, pady=0)
        self.rotate_az = Entry(axis_frame, textvariable=sRotateAz, width=3).pack(side=LEFT,padx=0, pady=0)
        
        self.rotate_b_label = Label(axis_frame, text="B:").pack(side=LEFT,padx=0,pady=0)
        self.rotate_bx = Entry(axis_frame, textvariable=sRotateBx, width=3).pack(side=LEFT,padx=0, pady=0)
        self.rotate_by = Entry(axis_frame, textvariable=sRotateBy, width=3).pack(side=LEFT,padx=0, pady=0)
        self.rotate_bz = Entry(axis_frame, textvariable=sRotateBz, width=3).pack(side=LEFT,padx=0, pady=0)

        self.degree_label = Label(axis_frame, text="Degree:").pack(side=LEFT,padx=0,pady=0)
        self.degree_spinbox = Spinbox(axis_frame, from_=0, to=360, width=3).pack(side=LEFT, padx=0, pady=0)

        self.steps_rotation_label = Label(axis_frame, text="Steps:").pack(side=LEFT,padx=0,pady=0)
        self.steps_rotation_spinbox = Spinbox(axis_frame, from_=0, to=10, width=3).pack(side=LEFT, padx=0, pady=0)

        self.rotate_button = Button(axis_frame, text="Rotate", fg="blue", command=self.rotate)
        self.rotate_button.pack(side=LEFT)                         

        scale_frame = Frame(master.ob_root_window)
        scale_frame.pack()

        i_scale = IntVar(value=1)
        self.scale_label = Label(scale_frame, text="Scale Ratio:").pack(side=LEFT,padx=0,pady=0)
        self.scale_all = Radiobutton(scale_frame, text="All", variable=i_scale, value=1).pack(side=LEFT,anchor=W)

        self.degree_spinbox = Spinbox(scale_frame, values=(0.25,0.50,0.75,1.00,1.25,1.50,1.75,2.00,2.25,2.50,2.75,3.00,3.25,3.50,3.75,4.00), width=3).pack(side=LEFT, padx=0, pady=0)
        self.scale_sxsysz = Radiobutton(scale_frame, text="[Sx,Sy,Sz]", variable=i_scale, value=2).pack(side=LEFT,anchor=W)

        fScaleSx = fDefaultOne
        sScaleSx = StringVar(value=str(round(fScaleSx,2)))
        fScaleSy = fDefaultOne
        sScaleSy = StringVar(value=str(round(fScaleSy,2)))
        fScaleSz = fDefaultOne
        sScaleSz = StringVar(value=str(round(fScaleSz,2)))

        fScaleAx = fDefaultZero
        sScaleAx = StringVar(value=str(round(fScaleAx,2)))
        fScaleAy = fDefaultZero
        sScaleAy = StringVar(value=str(round(fScaleAy,2)))
        fScaleAz = fDefaultZero
        sScaleAz = StringVar(value=str(round(fScaleAz,2)))
        
        self.scale_sx = Entry(scale_frame, textvariable=sScaleSx, width=3).pack(side=LEFT,padx=0, pady=0)
        self.scale_sy = Entry(scale_frame, textvariable=sScaleSy, width=3).pack(side=LEFT,padx=0, pady=0)
        self.scale_sz = Entry(scale_frame, textvariable=sScaleSz, width=3).pack(side=LEFT,padx=0, pady=0)

        self.scale_a_label = Label(scale_frame, text="Center of Scale:").pack(side=LEFT,padx=0,pady=0)

        self.scale_ax = Entry(scale_frame, textvariable=sScaleAx, width=3).pack(side=LEFT,padx=0, pady=0)
        self.scale_ay = Entry(scale_frame, textvariable=sScaleAy, width=3).pack(side=LEFT,padx=0, pady=0)
        self.scale_az = Entry(scale_frame, textvariable=sScaleAz, width=3).pack(side=LEFT,padx=0, pady=0)

        self.steps_rotation_label = Label(scale_frame, text="Steps:").pack(side=LEFT,padx=0,pady=0)
        self.steps_rotation_spinbox = Spinbox(scale_frame, from_=0, to=10, width=3).pack(side=LEFT, padx=0, pady=0)

        self.scale_button = Button(scale_frame, text="Scale", fg="blue", command=self.scale)
        self.scale_button.pack(side=LEFT)                         


        
    def browse_file(self):
        self.var_filename.set(filedialog.askopenfilename(filetypes=[("allfiles","*"),("pythonfiles","*.txt")]))
        filename = self.var_filename.get()

        # Save filename to 'mesh' object
        self.mesh.filename=filename
        print(filename)

    def load_file(self):
        # If there is a file to load (closing file dialog will return '')
        if(len(self.mesh.filename)):
            self.mesh.set_file(self.mesh.filename)
            self.mesh.load()
            
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

            # Call create_graphic_objects() method in 'wood_graphics_01.py'
            self.master.ob_world.create_graphic_objects(self.master.ob_canvas_frame.canvas,self.mesh)

            print ( "called the draw callback!")

    def rotate(self):
        print('rotate called')


    def scale(self):
        print('scale called')
            

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

