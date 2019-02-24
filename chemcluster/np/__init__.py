import numpy as np

class Nanoparticle:

    """
    This class involves all the tasks for processing nanoparticles.
    This class does not involve connection to the SQL database.
    """

    elements = []
    typelist = np.array([]).astype(int)
    coordinates = np.array([])

    @property
    def natoms(self):
        return len(self.coordinates)

    def __init__(self, xyz=None):
        if xyz is not None:
            self.load_xyz(xyz)

    def load_xyz(self, filename):
        self.elements, self.typelist, self.coordinates = self.get_xyz(filename)

    def to_xyz(self):
        assert self.natoms, "no nanoparticle loaded!"
        xyz = str(self.natoms)
        xyz += "\n"
        for i in range(self.natoms):
            xyz += ("\n" + self.elements[self.typelist[i]] + " " + " ".join(self.coordinates[i].astype(str).tolist()))
        return xyz

    def get_xyz(self, filename):
        with open(filename, 'r') as file:
            nAtoms = int(file.readline())
            coordinates = np.zeros((nAtoms, 3))
            typelist = np.zeros(nAtoms, dtype=int)
            elements = []

            file.readline()

            for i in range(nAtoms):
                line = file.readline().split()
                if line[0] not in elements:
                    elements.append(line[0])
                typelist[i] = elements.index(line[0])
                coordinates[i] = np.array(line[1:4], dtype=float)
        return elements, typelist, coordinates

    def get_surface_sites(self, element=None):
        Rall = self.coordinates
        Rin = self.coordinates
        if element is not None: Rin = self.typelist[self.typelist == element]
        Rm = self.get_surface_w_nn(Rin, Rall)
        Rsurf = self.get_surface_w_vector(Rm, Rall)
        return Rsurf

    def get_surface_w_nn(self, R_M, R_M_all, Rnb=3.0, chunkSize=100):
        nChunk = np.ceil(len(R_M) / chunkSize).astype(int)

        idxM = np.arange(len(R_M), dtype=int)
        Rsplit = np.array_split(R_M, nChunk)
        idxSpl = np.array_split(idxM, nChunk)
        isSurf = np.zeros(len(R_M), dtype=bool)

        for i in range(nChunk):
            numNb = np.sum(np.sum(((Rsplit[i])[:, np.newaxis, :] - R_M_all) ** 2, axis=2) < Rnb ** 2, axis=1)
            isSurf[(idxSpl[i])[numNb < 13]] = True
            print("Searching for surface sites using nearest neighbors, chunk", i + 1, "of ", nChunk)

        return R_M[isSurf]

    def get_surface_w_vector(self, R_surfNN, R_M_all, Rnb=15.0, angleCutoff=30):
        idxSurf = np.zeros(len(R_surfNN), dtype=bool)

        for i in range(len(R_surfNN)):
            d = np.sqrt(np.sum((R_surfNN[i] - R_M_all) ** 2, axis=1))
            R_M_nb = R_M_all[(d < Rnb) & (d != 0)] - R_surfNN[i]
            R_M_nb = R_M_nb / (np.sqrt(np.sum(R_M_nb ** 2, axis=1)))[:, np.newaxis]

            surfVec = -np.sum(R_M_nb, axis=0)
            surfVec = surfVec / np.linalg.norm(surfVec)

            angles = np.arccos(np.sum(surfVec * R_M_nb, axis=1)) * 180 / np.pi

            idxSurf[i] = (np.sum(angles < angleCutoff) == 0)
            print("Search for surface sites using surface vectors, site", i + 1, "of", len(R_surfNN))

        return R_surfNN[idxSurf]

    def get_clusters(self, surface_site=None, element=None, Rcut=8):
        if surface_site is None:
            surface_site = self.get_surface_sites(element)
        surface_site = np.array(surface_site).reshape((-1,3))
        for Rs in surface_site:
            Rl = Rs - self.coordinates
            dl = np.sqrt(np.sum(Rl**2, axis=-1))
            element_list = self.typelist[dl == 0].tolist()
            dl[dl>Rcut] = 0
            coord = Rl[dl>0]
            coord = np.concatenate([np.zeros((1,3)), coord], axis=0)
            element_list += self.typelist[dl>0].tolist()
            element_list = [self.elements[i] for i in element_list]
            assert len(coord) == len(element_list), "lengths between coord and element_list don't agree!"
            yield coord, element_list