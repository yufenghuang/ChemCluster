import os
import shutil

class QM:

    incar = ''
    kpoints = ''
    potcar = ''

    def __init__(self):
        pass

    def set_incar(self, incar):
        pass

    def set_potcar(self, incar):
        pass

    def set_kpoints(self, incar):
        pass

    def generate_vasp(self, poscar, directory, incar=None, kpoints=None, potcar=None):
        if incar == None and not self.incar: raise Exception("INCAR is not set")
        if kpoints == None and not self.kpoints: raise Exception("KPOINTS is not set")
        if potcar == None and not self.potcar: raise Exception("POTCAR is not set")

        if incar is None: kpoints = self.incar
        if kpoints is None: kpoints = self.kpoints
        if potcar is None: potcar = self.potcar

        if os.path.exists(directory):
            shutil.move(directory, directory+"_moved")

        os.mkdir(directory)
        with open(directory+"/INCAR", 'w') as f:
            f.write(incar)
        with open(directory+"/KPOINTS", 'w') as f:
            f.write(kpoints)
        with open(directory+"/POTCAR", 'w') as f:
            f.write(potcar)
        with open(directory+"/POSCAR", 'w') as f:
            f.write(poscar)

    def read_results(self, directory):
        pass

