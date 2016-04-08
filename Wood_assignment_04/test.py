from Wood_Object_04 import *
from Wood_Scene_04 import *
from Wood_Camera_04 import *
from Wood_Renderer_04 import *

o1 = Object()
o1.loadFile('C:/Users/Jeff/Dropbox/cse5365/assignments/Wood_assignment_04/cube_04.txt')
#print(' o.get() = ' + str(o.get()))

o2 = Object()
o2.loadFile('C:/Users/Jeff/Dropbox/cse5365/assignments/Wood_assignment_04/pyramid_04.txt')

s = Scene()
s.addObject(o1)
s.addObject(o1)
#print(' s.get() = ' + str(s.get()))

r = Renderer()
r.loadFile('C:/Users/Jeff/Dropbox/cse5365/assignments/Wood_assignment_04/cameras_04.txt')
r.addScene(s)
#print(' r.get() = ' + str(r.get()))
#print([k.vpn for k in r.cameras])

print(s.get()['points'])

print(s.get()['indices'])

