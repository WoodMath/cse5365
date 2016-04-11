# Wood, Jeff
# 100-103-5461
# 2016-04-19
# Assignment_04

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog

import string
from Wood_Clipping_04 import *
from Wood_Transform_04 import *
from Wood_Fileread_04 import *
from Wood_Widgets_04 import *
from Wood_Graphics_04 import *

def close_window_callback(root):

    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()


ob_root_window = Tk()
ob_root_window.protocol("WM_DELETE_WINDOW", lambda root_window=ob_root_window: close_window_callback(root_window))
ob_world=cl_world()
cl_widgets(ob_root_window,ob_world,ob_mesh)
ob_root_window.mainloop()    
    