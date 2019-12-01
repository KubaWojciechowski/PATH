import sys
import numpy as np
import Bio.PDB as pdb

parser = pdb.PDBParser()
structure = parser.get_structure('peptide', sys.argv[1])

structure.transform(translation=np.array((0, 0, 4),'f'))
io = pdb.PDBIO()

io.set_structure(structure)
io.save("test.pdb")
"""
new = pdb.StructureBuilder.StructureBuilder()

new.init_structure(1)
new.init_model(1)
new.init_chain('C')

for chain in structure.get_chains():
    resseq = 1
    for residue in structure.get_residues():
        print(residue.resname)
        print(resseq)
        new.init_residue(residue.resname, ' ', resseq, 'C')
        resseq += 1
        #for atom in structure.get_atoms():
    
nstruct = new.get_structure()

for i in nstruct.get_residues():
    print(i)
"""
