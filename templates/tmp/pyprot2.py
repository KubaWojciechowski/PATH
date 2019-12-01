import sys
import pdbio

def translate(atoms, vector):
    """
    Translate given atoms by a vector

    atoms  - dictionary of atoms
    vector - vector in form of list or tuple
    """
    for atom in atoms:
        atom['x'] = atom['x'] + vector[0]
        atom['y'] = atom['y'] + vector[1]
        atom['z'] = atom['z'] + vector[2]

    return atoms


def chainName(atoms, oldName, newName):
    """Chnage name of chain in PDB file"""

    for atom in atoms:
        if atom['chain'] == oldName:
            atom['chain'] = newName

    return atoms


if __name__ == '__main__':

    atoms = pdbio.readPDB(sys.argv[1])
   
    oldName1 = 'A'
    oldName2 = 'B'
    oldName3 = 'C'
    oldName4 = 'D'

    for i in [('E','F','G','H'),('I','J','K','L'),('M','N','O','P')]:
        
        x = 4.8*2
        y = 0
        z = 0

        new = translate(atoms,(x, y, z))
        
        newName1 = i[0]
        newName2 = i[1]
        newName3 = i[2]
        newName4 = i[3]

        new = chainName(new, oldName1, newName1)
        new = chainName(new, oldName2, newName2)
        new = chainName(new, oldName3, newName3)
        new = chainName(new, oldName4, newName4)

        pdbio.writePDB("test"+i[0]+i[1]+".pdb", new)

        x += x
        oldName1 = newName1
        oldName2 = newName2
        oldName3 = newName3
        oldName4 = newName4

