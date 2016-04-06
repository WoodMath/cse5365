from Wood_Object_04 import *
from Wood_Scene_04 import *
from Wood_Camera_04 import *
from Wood_Renderer_04 import *

o = Object()
o.loadFile('C:/Users/Jeff/Dropbox/cse5365/assignments/Wood_assignment_04/cube_04.txt')
#print(' o.get() = ' + str(o.get()))

s = Scene()
s.addObject(o)
#print(' s.get() = ' + str(s.get()))

r = Renderer()
r.loadFile('C:/Users/Jeff/Dropbox/cse5365/assignments/Wood_assignment_04/cameras_04.txt')
r.addScene(s)
#print(' r.get() = ' + str(r.get()))
#print([k.vpn for k in r.cameras])





