# Wood, Jeff
# 100-103-5461
# 2016-02-17
# Assignment_01
#!/~/anaconda3/bin/python3.5

#   From:
#       http://stackoverflow.com/questions/15599639/whats-perfect-counterpart-in-python-for-while-not-eof
#       http://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
#       http://stackoverflow.com/questions/7118276/how-to-remove-specific-element-in-an-array-using-python
#       http://stackoverflow.com/questions/379906/parse-string-to-float-or-int
#       http://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index-in-python
#       http://docs.scipy.org/doc/numpy/reference/generated/numpy.dot.html#numpy.dot
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.vectorize.html
#       http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.matrix.transpose.html
#       http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.array.html
#
#       http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_polygon.html
#       http://zetcode.com/gui/tkinter/drawing/
#       http://effbot.org/tkinterbook/canvas.htm

#import pip
#installed_packages = pip.get_installed_distributions()
#installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
#    for i in installed_packages])
#print(installed_packages_list)

#print(dot([1, 2, 3],[4,5,6]))


import numpy as np

class number_range:
    def __init__(self,vMin,vMax):
        self.min=vMin
        self.max=vMax
    def set_number_range(self,vMin,vMax):
        self.min=vMin
        self.max=vMax        

def single_int(passed_int):
    return int(passed_int)
def single_int_less_one(passed_int):
    return int(passed_int)-1
def single_float(passed_float):
    return float(passed_float)

vect_int=np.vectorize(int)
vect_int_less_one=np.vectorize(single_int_less_one)
vect_float=np.vectorize(float)

class mesh:
    def __init__(self):
        self.vertices=[]
        self.faces=[]
        self.wx=[]
        self.wy=[]
        self.vx=[]
        self.vy=[]
        self.filename=None
    def set_file(self,filename):
        self.vertices=[]
        self.faces=[]
        self.wx=[]
        self.wy=[]
        self.vx=[]
        self.vy=[]
        self.filename=filename
    def add_vertex(self,vertex):
        self.vertices.append(vertex)
    def add_face(self,face):
        self.faces.append(face)
    def add_window(self,window):
        self.wx=[window[0],window[2]]
        self.wy=[window[1],window[3]]
    def add_viewport(self,viewport):
        self.vx=[viewport[0],viewport[2]]
        self.vy=[viewport[1],viewport[3]]
    def load(self):
        with open(self.filename) as openfileobject:
            for line in openfileobject:
                print(line,end='')
                line_parsed=line.split()
                if(len(line_parsed)>0):
                    line_type=line_parsed[0]
                    line_parsed.pop(0)
                    if(line_type=='v'):
                        line_parsed=vect_float(line_parsed)
                        self.add_vertex(line_parsed)
                    if(line_type=='f'):
                        line_parsed=vect_int_less_one(line_parsed[:])
                        self.add_face(line_parsed)
                    if(line_type=='w'):
                        line_parsed=vect_float(line_parsed[:])
                        self.add_window(line_parsed)
                    if(line_type=='s'):
                        line_parsed=vect_float(line_parsed[:])
                        self.add_viewport(line_parsed)

    

#m=mesh()
#m.set_file('/home/jeff/Dropbox/cse5365/assignments/Wood_assignment_01/teapot_01.txt')
#m.load()

