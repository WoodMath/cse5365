# Wood, Jeff
# 100-103-5461
# 2016-04-19
# Assignment_04

from tkinter import *
from math import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk

from Wood_Fileread_04 import *

class cl_widgets:
    def __init__(self,ob_root_window, ob_world,ob_controller):
        self.ob_root_window=ob_root_window
        self.ob_world = ob_world
        self.controller = ob_controller                     ## Set by controller 'addView' method

        self.panel = cl_panel(self)
        self.ob_canvas_frame = cl_canvas_frame(self)
        self.ob_world.add_canvas(self.ob_canvas_frame.canvas)


class cl_canvas_frame:
    def __init__(self, master):        
        self.master = master
        self.controller =  master.controller                ## Set by controller 'addView' method
        

        self.canvas = Canvas(master.ob_root_window, width=640, height=640, bg="yellow", highlightthickness=0)
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
        #self.canvas.config(width=event.width-4,height=event.height-4)
        #print 'canvas width height', self.canvas.cget("width"), self.canvas.cget("height")
        #print 'event width height',event.width, event.height
        
        self.canvas.pack()
        
        self.master.ob_world.redisplay_graphic_objects()

class cl_panel:
    def __init__(self, master):
        self.master = master
        self.canvas = master.ob_root_window
        self.world = master.ob_world
        self.controller =  master.controller                ## Set by controller 'addView' method
        
        self.drawGUIwidgets()
        
    def drawGUIwidgets(self):
        master = self.master
        file_frame = Frame(master.ob_root_window)
        file_frame.pack()


        #############
        ## 1st Row ##
        #############
        
        self.filename = StringVar()
        self.file_location_label = Label(file_frame, text="File Name:")
        self.file_location_label.pack(side=LEFT,padx=10,pady=10)
        self.file_location_string = Entry(file_frame, text="File Name:", textvariable=self.filename, width=50)
        self.file_location_string.pack(side=LEFT,padx=0, pady=0)
#        self.file_location_string = Label(file_frame, textvariable=self.filename, width=50).pack(side=LEFT,padx=0,pady=0)
        
        self.file_dialog_button = Button(file_frame, text="Browse", fg="blue", command=self.browse_file)
        self.file_dialog_button.pack(side=LEFT)        

        self.var_filename = StringVar()
        self.var_filename.set('')
        self.button = Button(file_frame, text="Load", fg="red", command=self.load_file)
        self.button.pack(side=LEFT)


        #############
        ## 2nd Row ##
        #############

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
        self.fDefaultTen = 10.0
        
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

        self.sRotateDegrees=StringVar(value='90')
        self.rotate_degrees_label = Label(axis_frame, text="Degree:").pack(side=LEFT,padx=0,pady=0)
        self.rotate_degrees_spinbox = Spinbox(axis_frame, from_=-360, to=360, width=3, textvariable=self.sRotateDegrees)
        self.rotate_degrees_spinbox.delete(0,"end")
        self.rotate_degrees_spinbox.insert(0,"90")
        self.rotate_degrees_spinbox.pack(side=LEFT, padx=0, pady=0)

        self.sRotateSteps=StringVar(value='1')
        self.rotate_steps_label = Label(axis_frame, text="Steps:").pack(side=LEFT,padx=0,pady=0)
        self.rotate_steps_spinbox = Spinbox(axis_frame, from_=0, to=10, width=3, textvariable=self.sRotateSteps)
        self.rotate_steps_spinbox.delete(0,"end")
        self.rotate_steps_spinbox.insert(0,"1")
        self.rotate_steps_spinbox.pack(side=LEFT, padx=0, pady=0)

        self.rotate_button = Button(axis_frame, text="Rotate", fg="green", command=self.rotate)
        self.rotate_button.pack(side=LEFT)                         

        #############
        ## 3rd Row ##
        #############

        scale_frame = Frame(master.ob_root_window)
        scale_frame.pack()

        self.i_scale_option = IntVar(value=1)
        self.scale_label = Label(scale_frame, text="Scale Ratio:").pack(side=LEFT,padx=0,pady=0)
        self.scale_all = Radiobutton(scale_frame, text="All", variable=self.i_scale_option, value=1).pack(side=LEFT,anchor=W)

        self.sScaleSize = StringVar(value="1.00")
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

        self.sScaleSteps = StringVar(value='1')
        self.scale_steps_label = Label(scale_frame, text="Steps:").pack(side=LEFT,padx=0,pady=0)
        self.scale_steps_spinbox = Spinbox(scale_frame, from_=0, to=10, width=3, textvariable=self.sScaleSteps)
        self.scale_steps_spinbox.delete(0,"end")
        self.scale_steps_spinbox.insert(0,"1")
        self.scale_steps_spinbox.pack(side=LEFT, padx=0, pady=0)

        self.scale_button = Button(scale_frame, text="Scale", fg="green", command=self.scale)
        self.scale_button.pack(side=LEFT)

        #############
        ## 4th Row ##
        #############

        trans_frame = Frame(master.ob_root_window)
        trans_frame.pack()

        self.fTransTx = self.fDefaultOne
        self.sTransTx = StringVar(value=str(round(self.fTransTx,2)))
        self.fTransTy = self.fDefaultOne
        self.sTransTy = StringVar(value=str(round(self.fTransTy,2)))
        self.fTransTz = self.fDefaultOne
        self.sTransTz = StringVar(value=str(round(self.fTransTz,2)))

        self.trans_label = Label(trans_frame, text="Translation ([dx,dy,dz]):").pack(side=LEFT,padx=0,pady=0)

        self.trans_tx = Entry(trans_frame, textvariable=self.sTransTx, width=3).pack(side=LEFT,padx=0, pady=0)
        self.trans_ty = Entry(trans_frame, textvariable=self.sTransTy, width=3).pack(side=LEFT,padx=0, pady=0)
        self.trans_tz = Entry(trans_frame, textvariable=self.sTransTz, width=3).pack(side=LEFT,padx=0, pady=0)

        self.sTransSteps = StringVar(value='1')
        self.trans_steps_label = Label(trans_frame, text="Steps:").pack(side=LEFT,padx=0,pady=0)
        self.trans_steps_spinbox = Spinbox(trans_frame, from_=0, to=10, width=3, textvariable=self.sTransSteps)
        self.trans_steps_spinbox.delete(0,"end")
        self.trans_steps_spinbox.insert(0,"1")
        self.trans_steps_spinbox.pack(side=LEFT, padx=0, pady=0)

        self.trans_button = Button(trans_frame, text="Translate", fg="green", command=self.translate)
        self.trans_button.pack(side=LEFT)                         

        #############
        ## 5th Row ##
        #############

        vrp_frame = Frame(master.ob_root_window)
        vrp_frame.pack()

        self.camera_label = Label(vrp_frame, text="Camera:").pack(side=LEFT,padx=0,pady=0)
        self.sCamera = StringVar()
        self.lCameras = [c.info for c in self.controller.renderer.cameras]
        self.tCameras = tuple(self.lCameras)
        self.camera = ttk.Combobox(vrp_frame, text="Camera", values=self.tCameras, width=10)
        self.camera.bind("<<ComboboxSelected>>", self.camera_selected)
        self.camera.pack(side=LEFT,padx=0, pady=0)
        self.camera.current(0)
        self.camera.pack()

       
        self.fVRPAx = self.fDefaultZero
        self.sVRPAx = StringVar(value=str(round(self.fVRPAx,2)))
        self.fVRPAy = self.fDefaultZero
        self.sVRPAy = StringVar(value=str(round(self.fVRPAy,2)))
        self.fVRPAz = self.fDefaultZero
        self.sVRPAz = StringVar(value=str(round(self.fVRPAz,2)))
        
        self.vrp_a_label = Label(vrp_frame, text="VRP A([x,y,z]):").pack(side=LEFT,padx=0,pady=0)
        self.vrp_ax = Entry(vrp_frame, textvariable=self.sVRPAx, width=3)
        self.vrp_ax.pack(side=LEFT,padx=0, pady=0)
        self.vrp_ay = Entry(vrp_frame, textvariable=self.sVRPAy, width=3)
        self.vrp_ay.pack(side=LEFT,padx=0, pady=0)
        self.vrp_az = Entry(vrp_frame, textvariable=self.sVRPAz, width=3)
        self.vrp_az.pack(side=LEFT,padx=0, pady=0)

        self.fVRPBx = self.fDefaultOne
        self.sVRPBx = StringVar(value=str(round(self.fVRPBx,2)))
        self.fVRPBy = self.fDefaultOne
        self.sVRPBy = StringVar(value=str(round(self.fVRPBy,2)))
        self.fVRPBz = self.fDefaultOne
        self.sVRPBz = StringVar(value=str(round(self.fVRPBz,2)))
        
        self.vrp_b_label = Label(vrp_frame, text="VRP B([x,y,z]):").pack(side=LEFT,padx=0,pady=0)
        self.vrp_bx = Entry(vrp_frame, textvariable=self.sVRPBx, width=3)
        self.vrp_bx.pack(side=LEFT,padx=0, pady=0)
        self.vrp_by = Entry(vrp_frame, textvariable=self.sVRPBy, width=3)
        self.vrp_by.pack(side=LEFT,padx=0, pady=0)
        self.vrp_bz = Entry(vrp_frame, textvariable=self.sVRPBz, width=3)
        self.vrp_bz.pack(side=LEFT,padx=0, pady=0)
        
        self.sFlySteps = StringVar(value='1')
        self.fly_steps_label = Label(vrp_frame, text="Steps:").pack(side=LEFT,padx=0,pady=0)
        self.fly_steps_spinbox = Spinbox(vrp_frame, from_=0, to=10, width=3, textvariable=self.sFlySteps)
        self.fly_steps_spinbox.delete(0,"end")
        self.fly_steps_spinbox.insert(0,"1")
        self.fly_steps_spinbox.pack(side=LEFT, padx=0, pady=0)

        self.fly_button = Button(vrp_frame, text="Fly", fg="green", command=self.fly)
        self.fly_button.pack(side=LEFT)                         
        
        disc_frame_thr = Frame(master.ob_root_window)
        disc_frame_thr.pack()
        self.disc_label_thr = Label(disc_frame_thr, text="NOTE: Transformations are cumulative. Click 'Load' to reset transformation stack.")
        self.disc_label_thr.pack(side=LEFT,padx=0,pady=0)

        self.updateVRPs()

    def camera_selected(self,event):

        self.controller.saveFormValues()
        self.updateVRPs()


    def updateVRPs(self):
        v_vrpA = self.controller.getCameraVRP_A()
        v_vrpB = self.controller.getCameraVRP_B()

        self.vrp_ax.delete(0,"end")
        self.vrp_ax.insert(0,'%.1f' % v_vrpA[0])
        self.vrp_ay.delete(0,"end")
        self.vrp_ay.insert(0,'%.1f' % v_vrpA[1])
        self.vrp_az.delete(0,"end")
        self.vrp_az.insert(0,'%.1f' % v_vrpA[2])

        self.vrp_bx.delete(0,"end")
        self.vrp_bx.insert(0,'%.1f' % v_vrpB[0])
        self.vrp_by.delete(0,"end")
        self.vrp_by.insert(0,'%.1f' % v_vrpB[1])
        self.vrp_bz.delete(0,"end")
        self.vrp_bz.insert(0,'%.1f' % v_vrpB[2])
        
    def browse_file(self):
        self.var_filename.set(filedialog.askopenfilename(filetypes=[("allfiles","*"),("pythonfiles","*.txt")]))
        filename = self.var_filename.get()        

        self.filename.set(filename)        
 
        self.file_location_string.delete(0,"end");
        self.file_location_string.insert(0, self.var_filename.get())

        self.controller.saveFormValues()

    def load_file(self):
        ## Make sure everythin displayed in forms is saved
        self.controller.saveFormValues()
        
        if(not len(self.controller.fileName)):
            return
        
        self.controller.loadObject()
        

            
    def rotate(self):
        ## Make sure everythin displayed in forms is saved
        self.controller.saveFormValues()

        print(' Rotate button pushed ')

    def scale(self):
        ## Make sure everythin displayed in forms is saved
        self.controller.saveFormValues()

        print(' Scale button clicked ')

    def translate(self):
        ## Make sure everythin displayed in forms is saved
        self.controller.saveFormValues()

        print(' Translate button clicked ')

    def fly(self):
        ## Make sure everythin displayed in forms is saved
        self.controller.saveFormValues()

        print(' Fly button clicked ')

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


#class StatusBar:

    #def __init__(self, master):
        #self.master=master
        #self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        #self.label.pack(fill=X)

    #def set(self, format, *args):
        #self.label.config(text=format % args)
        #self.label.update_idletasks()

    #def clear(self):
        #self.label.config(text="")
        #self.label.update_idletasks()       

