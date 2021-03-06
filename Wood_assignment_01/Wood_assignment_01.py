# Wood, Jeff
# 100-103-5461
# 2016-02-17
# Assignment_01

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog

import string
from wood_fileread_01 import *
from wood_widgets_01 import *
from wood_graphics_01 import *


def close_window_callback(root):
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()


ob_mesh=mesh()
ob_root_window = Tk()
ob_root_window.protocol("WM_DELETE_WINDOW", lambda root_window=ob_root_window: close_window_callback(root_window))
ob_world=cl_world(ob_mesh)
cl_widgets(ob_root_window,ob_world,ob_mesh)
ob_root_window.mainloop()    
    
