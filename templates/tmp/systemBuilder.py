#!/usr/bin/python3
#Program to build system from one pdb file
import sys

def move(filename, movex, movey, movez, chain, mvfile):

	file = open(filename)
	pdb = file.read()
	file.close()
	#delete header
	lines = pdb.splitlines()
	del lines[0:2]
	#Get and change x coordinate
	for i in range(0,len(lines)):
		if lines[i][0:4] == 'ATOM':
			linestart = lines[i][0:30]
			lineend = lines[i][54:]
			x = float(lines[i][31:38])
			y = float(lines[i][38:47])
			z = float(lines[i][47:55])
			newx = x+movex
			newy = y+movey
			newz = z+movez
			newx = "%8.3f" % newx
			newy = "%8.3f" % newy
			newz = "%8.3f" % newz
			newx = str(newx)
			newy = str(newy)
			newz = str(newz)
			lines[i] = linestart+newx+newy+newz+lineend
	#Change name of chain
	for i in range(0,len(lines)):
		if lines[i][0:4] == 'ATOM':
			lines[i]=lines[i].replace(' A ', ' '+chain+' ')
	#Join lines
	newpdb = '\n'.join(lines)
	print(newpdb)
	newfile = open(mvfile,'w')
	newfile.write(newpdb)
	newfile.close()

if __name__ == '__main__':

    movex=float(sys.argv[2])
    movey=float(sys.argv[3])
    movez=float(sys.argv[4])
    name = sys.argv[1].split('_')[0] + '_'

    for i in ['X']:
        move(sys.argv[1], movex, movey, movez, i, name+i+'.pdb')
        #movex += 0
        #movey += 25
        #movez += 0
	




