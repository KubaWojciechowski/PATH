import urllib.request
import io

def parsePDB(data):

	line=data.readline()

	atom_list=[]
	while line:
		if line.startswith('ATOM  ') or line.startswith('HETATM'):
			
			atom_name = line[12:16].strip()
			atom_index = int(line[6:11])
			atom_resname = line[17:20]
			atom_resid = int(line[22:26])
			atom_chain = line[21]
			atom_x = float(line[30:38])
			atom_y = float(line[38:46])
			atom_z = float(line[46:54])
			
			atom = {
					'index' : atom_index,
					'name' : atom_name,
					'resname' : atom_resname,
					'resid' : atom_resid,
					'chain' : atom_chain,
					'x' : atom_x,
					'y' : atom_y,
					'z' : atom_z
					}
					
			atom_list.append(atom)
			
		line=data.readline()
	
	data.close()
	return(atom_list)

# Function readPDB reads atoms (sections ATOM and HETATM
# from a PDB file and returns a list of atoms. Each atom
# is a dictionary or namedtuple
#
# Input: file name (str)
# Output: list of dictionaries or named tuples

def readPDB(filename):
	data=open(filename)
	all_atoms = parsePDB(data)
	data.close()
	return(all_atoms)


# Function dowloadPDB uses urllib.request to download
# a PDB file from PDB database and returns a list of atoms.
# Each atom is a dictionary or namedtuple
#
# Consider writing a common backend function for readPDB
# and downloadPDB!
#
# Input: PDBID (str)
# Output: list of dictionaries or named tuples
def downloadPDB(code):
	
	url = 'https://files.rcsb.org/download/%s.pdb' % code
	
	remote = urllib.request.urlopen(url)
	
	if remote.status != 200:
		raise RuntimeError('%s is not available') % url
		
	data = io.TextIOWrapper(remote, 'ASCII')
	
	all_atoms = parsePDB(data)
	
	remote.close()
	
	return(all_atoms)
	
'''
data = downloadPDB('1PEF')
for i in  data:
	print(i)
'''

# Input: list of dictionaries or named tuples
# Output: none
def writePDB(filename, all_atoms):
	
	f=open(filename,'w')
	
	for i in all_atoms:
		f.write("%s %4i %3s %4s %1s %3i %s %7.3f %7.3f %7.3f %s %s \n" % ('ATOM  ',
                                                                    i['index'], 
                                                                    i['name'], 
                                                                    i['resname'], 
                                                                    i['chain'],
                                                                    i['resid'],
                                                                    '   ',
                                                                    i['x'],
                                                                    i['y'],
                                                                    i['z'],
                                                                    ' 1.00',
                                                                    ' 1.00'))

	f.close()
#data = downloadPDB('1PEF')
#writePDB('test.pdb',data)

# Generator
# Input: list of dictionaries or named tuples
# Output: dictionary or named tuple
def filterAtoms(all_atoms, field, value):
    
    for i in all_atoms:
    	if i[field] == value:
    		yield i


if __name__ == '__main__':

    data = readPDB("class1.pdb")		

    for i in data:
	    print(i)


    writePDB("test.pdb", data)
