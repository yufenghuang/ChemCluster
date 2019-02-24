import os
import shutil
import numpy as np

class QM:

    incar = ''
    kpoints = ''
    potcar = ''

    def __init__(self, incar="None", potcar="None", kpoints="None"):
        if incar is not None: self.set_incar(incar)
        if potcar is not None: self.set_potcar(potcar)
        if kpoints is not None: self.set_kpoints(kpoints)

    def set_incar(self, incar):
        self.incar = incar

    def set_potcar(self, potcar):
        self.potcar = potcar

    def set_kpoints(self, kpoints):
        self.kpoints = kpoints

    def generate_vasp(self, poscar, directory, incar=None, kpoints=None, potcar=None):
        if incar is None and not self.incar: raise Exception("INCAR is not set")
        if kpoints is None and not self.kpoints: raise Exception("KPOINTS is not set")
        if potcar is None and not self.potcar: raise Exception("POTCAR is not set")

        if incar is not None: self.set_incar(incar)
        if potcar is not None: self.set_potcar(potcar)
        if kpoints is not None: self.set_kpoints(kpoints)

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

    def generate_poscar(self, coordinates, elements, lattice=20,
                        lattice_scaling=1.0, centering=False,
                        selective_dynamics=False, molecule=""):
        if type(coordinates) is str:
            coordinates = np.array(coordinates.split(" "), dtype=float).reshape(-1, 3)

        # Comment
        poscar = "POSCAR generated from ChemCluster\n"

        # Scaling (of the lattice vector, not the coordinate)
        poscar += str(lattice_scaling) + "\n"

        # Lattice vectors
        if type(lattice) in [int, float]:
            lattice = np.eye(3)*lattice
        elif len(lattice) == 3:
            lattice = np.diag(lattice).astype(np.float64)
        else:
            lattice = np.array(lattice)
        for i in range(3):
            poscar += " ".join([str(l) for l in lattice[i].tolist()]) + "\n"

        # Element list
        if type(elements) is list:
            assert len(elements)==len(coordinates), \
                "The lenghs of 'elements' and 'coordinates' must match if 'elements' is a list"
        else:
            elements = [elements] * len(coordinates)

        # Adsorbed molecule
        if molecule == "CO":
            vector = coordinates.sum(axis=0)
            vector = -vector / np.sqrt(np.sum(vector ** 2))
            C = vector * 1.86
            O = vector * 3.02
            CO = np.array([C, O])
            elements = ['C', 'O'] + elements
            coordinates = np.concatenate([CO, coordinates], axis=0)

        # Element list (printing)
        poscar += " ".join(set(elements)) + "\n"
        poscar += " ".join([str(elements.count(e)) for e in set(elements)]) + "\n"

        # Selective dynamics
        selective = [" "] * len(elements)
        if selective_dynamics:
            poscar += "Selective Dynamics\n"
            selective = [" F F F "] * len(elements)
            if molecule == "CO": selective[0] = selective[1] = " T T T "

        # Coordinates
        if centering:
            center = lattice.sum(axis=0)/2
            coordinates += center
        poscar += "Cartesian\n"
        for e in set(elements):
            R = coordinates[np.array(elements) == e]
            s = np.array(selective)[np.array(elements) == e]
            for i in range(len(R)):
                poscar += " ".join([str(r) for r in R[i]]) + s[i] + " \n"

        return poscar

    def read_results(self, directory):
        pass

