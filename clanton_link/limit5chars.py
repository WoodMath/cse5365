#!/usr/bin/env python
import Tkinter as tk

master = tk.Tk()

def callback():
    print e.get()

def val(i):
    print "validating"
    print i

    if int(i) > 4:
        print "False"
        return False
    return True

vcmd = (master.register(val), '%i')

e = tk.Entry(master, validate="key", validatecommand=vcmd)
e.pack()

b = tk.Button(master, text="OK", command=lambda: callback())
b.pack()

tk.mainloop()
