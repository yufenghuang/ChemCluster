import numpy as np
import torch

class Nanoparticle:

    """
    This class involves all the tasks for processing nanoparticles.
    This class does not involve connection to the SQL database.
    """

    elements = []
    typelist = []
    coordinates = np.array([])

    def __init__(self, xyz=None):
        if xyz is not None:
            self.load_xyz(xyz)

    def load_xyz(self, filename):
        self.elements, self.typelist, self.coordinates = self.get_xyz(filename)

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

    def get_clusters(self, surface_site=None, element=None):
        pass

