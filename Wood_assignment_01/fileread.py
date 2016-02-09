#!~/anaconda3/bin/python3.5
# From:
#       http://stackoverflow.com/questions/15599639/whats-perfect-counterpart-in-python-for-while-not-eof

with open('pyramid_01.txt') as openfileobject:
    for line in openfileobject:
        k=line.split()
        print(k)
        print(len(k))
        #print(line,end='')
