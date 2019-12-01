#!/home/kuba/anaconda3/bin/python3
import sys

pdb = open(sys.argv[1])
name = sys.argv[1].split('.')[0] + '_num.pdb'
newpdb =open(name, 'w')
clist = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

c = 0
for i in pdb:
    
    if i[0:5] == 'CRYST':
        print(i, file=newpdb, end='')

    if i[0:4] == 'ATOM':
        if i[24:26] == ' 1' and i[13] == 'N':
           c += 1

        lstart = i[0:21]
        lend = i[22:]
        print(lstart+clist[c]+lend, file=newpdb, end='')

pdb.close()
newpdb.close()
