from modeller import *
from modeller.automodel import *    # Load the automodel class

#log.verbose()

# Override the 'special_restraints' and 'user_after_single_model' methods:
class MyModel(automodel):
    def special_restraints(self, aln):
        # Constrain the A and B chains to be identical (but only restrain
        # the C-alpha atoms, to reduce the number of interatomic distances
        # that need to be calculated):
        s1 = selection(self.chains['A']).only_atom_types('CA')
        s2 = selection(self.chains['B']).only_atom_types('CA')
        self.restraints.symmetry.append(symmetry(s1, s2, 1.0))
    def user_after_single_model(self):
        # Report on symmetry violations greater than 1A after building
        # each model:
        self.restraints.symmetry.report(1.0)

env = environ()
# directories for input atom files
env.io.atom_files_directory = ['.', '../atom_files']

# Be sure to use 'MyModel' rather than 'automodel' here!
a = MyModel(env,
            alnfile  = 'alignment.pir' ,     # alignment filename
            knowns   = 'template',          # codes of the templates
            sequence = 'sequence',
		    assess_methods = (assess.DOPE, assess.GA341))            # code of the target

a.starting_model= 1                # index of the first model
a.ending_model  = 10              # index of the last model
                               # (determines how many models to calculate)
#a.md_level = refine.slow           # Better MD
a.make()                           # do comparative modeling

