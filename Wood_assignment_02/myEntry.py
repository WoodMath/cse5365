#!/usr/bin/env python
from Tkinter import *

class MyEntry(Entry):

    def __init__(self, master, maxchars):
        Entry.__init__(self, master, validate = "key",    validatecommand=self.validatecommand)
        self.MAX = maxchars

    def validatecommand(self, *args):
        if len(self.get()) >= self.MAX:
            self.delete(0,3)
            self.insert(0, "no")
        return True

if __name__ == '__main__':
    tkmain = Tk()
    e = MyEntry(tkmain, 5)
    e.grid()
    tkmain.mainloop()
