import os
import pyrosetta as pr
from pyrosetta.toolbox import cleanATOM
pr.init()

def eTerms(pose):
    """Calclulate energy terms for pose"""

    energy = {}
    for scoretype in scorefxn.get_nonzero_weighted_scoretypes():
        energy[str(scoretype).split('.')[1]] = pose.energies().total_energies()[scoretype]

    return energy


def getScore(path):
    """Calculate pyRosetta score"""
    # Clean PDB files
    cleanATOM(path)
    # Clean struct name
    cleanName = path[0:-3]+'clean'+'.pdb'

    pose = pr.pose_from_pdb(cleanName)

    tmp = scorefxn(pose)
    energy = eTerms(pose)
    energy['ref15'] = tmp

    os.remove(cleanName)
    
    return energy


def writeLine(fileName,seq,aclass,model,energy):
    """Write restults to csv file"""

    
    print("%s,%s,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f" %
            (seq,aclass,model,energy['ref15'],energy['fa_atr'],
            energy['fa_rep'],energy['fa_sol'],energy['fa_intra_rep'],
            energy['fa_intra_sol_xover4'],energy['lk_ball_wtd'],
            energy['fa_elec'],energy['omega'],energy['fa_dun'],
            energy['p_aa_pp'],energy['yhh_planarity'],
            energy['ref'],energy['rama_prepro']), file=fileName)


if __name__ == '__main__':

    scorefxn = pr.get_fa_scorefxn()

    f = open("pyrosetta.csv",'w')

    print("seq,class,model,ref15,fa_atr,fa_rep,fa_sol,fa_intra_rep,fa_intra_sol_xover4,lk_ball_wtd,fa_elec,omega,fa_dun,p_aa_pp,yhh_planarity,ref,rama_prepro",file = f)

    ### Loop over files in results directories ###
    for seq in os.listdir('.'):
        if os.path.isdir(seq) and not seq[0] == '.':
            print(seq)

            for classDir in os.listdir(seq):
                print(classDir)

                path = seq+'/'+classDir

                for struct in os.listdir(path):
                    if struct.endswith(".pdb") and struct.startswith("sequence"):
                       
                        sFile = struct
                        modelNum = int(struct.split('.')[1][-3:])

                        os.chdir(path)

                        energy = getScore(struct)

                        writeLine(f,seq,classDir[-1],modelNum,energy)

                        os.chdir('../../')

    f.close()

"""
    scorefxn = pr.get_fa_scorefxn()
   
    f = open("pyrosetta.csv",'w')

    path = "sequence.B99990001.pdb"

    energy = getScore(path)

    modelNum = int(path.split('.')[1][-3:])

    print("seq,class,model,ref15,fa_atr,fa_rep,fa_sol,fa_intra_rep,fa_intra_sol_xover4,lk_ball_wtd,fa_elec,omega,fa_dun,p_aa_pp,yhh_planarity,ref,rama_prepro",file = f)
    
    writeLine(f,'SEQ','aclass',1,energy)
    f.close()
"""
