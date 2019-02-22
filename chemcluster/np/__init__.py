import numpy as np
import torch

class Nanoparticle:

    """
    This class involves all the tasks for processing nanoparticles.
    This class does not involve connection to the SQL database.
    """

    elements = []
    atomtypes = []
    coordinates = np.array([])

    def __init__(self, xyz=None):
        if xyz is not None:
            self.read_xyz(xyz)

    def read_xyz(self, filename):
        pass

    def get_surface_sites(self, element_list=None):
        pass

    def get_clusters(self, surface_site=None, element_list=None):
        pass

