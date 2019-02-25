from .sql import SQLHandler
from .np import Nanoparticle
from .qm import QM

import random
import os
import shutil

class CC:
    '''
        This is the main object to perform tasks on ChemCluster
    '''

    sql_h = SQLHandler()
    nanoparticle = Nanoparticle()
    qm = QM()
    kpoints_id=None
    incar_id=None

    def __init__(self, config_file=''):
        if config_file:
            self.sql_h = SQLHandler(config_file)

    def show_databases(self):
        pass

    #######################################################
    # SQL connection
    #######################################################

    def is_connected(self):
        """
        Check whether the SQL database is connected
        :return: True or False
        """
        return self.sql_h.is_connected()

    def connect(self, config_file):
        """
        Connect to the mysql database given the information provided in the config_file
        :param config_file: location of the config_file to connect to the SQL database
        :return: None
        """
        self.sql_h.connect(config_file)

    def disconnect(self):
        """
        Disconnect from the SQL database
        :return: None
        """
        self.sql_h.disconnect()

    #######################################################
    # Nanoparticles database
    #######################################################

    def load_np(self, xyzfile):
        self.nanoparticle = Nanoparticle(xyzfile)

    def add_np(self, description, xyzfile=None, element=None, Rcut=8):
        if xyzfile is not None: self.nanoparticle.load_xyz(xyzfile)
        assert self.nanoparticle.natoms, "no nanoparticle loaded!"
        natoms = self.nanoparticle.natoms
        cluster_gen = self.nanoparticle.get_clusters(element, Rcut=Rcut)
        self.sql_h.insert("INSERT INTO Nanoparticles VALUES (%s, %s, %s, %s, %s)",
                          (None, str(natoms), description, " ".join(self.nanoparticle.elements), self.nanoparticle.to_xyz()))
        np_ID = self.sql_h.query("SELECT ID FROM Nanoparticles ORDER BY ID DESC LIMIT 1")[0][0]
        surface_sites = [(None, np_ID, str(len(c)), str(Rcut), " ".join(set(e)), " ".join(e),
                          " ".join(c.reshape(-1).astype(str).tolist())) for c, e in cluster_gen]
        self.sql_h.insertmany("INSERT INTO SurfaceSites VALUES (%s, %s, %s, %s, %s, %s, %s)", surface_sites)

    def show_np(self, id=None):
        if id is not None:
            query = "SELECT id, Description, Elements, Coordinates FROM Nanoparticle WHERE id="+str(id)
            rows = self.sql_h.query(query)
            for row in rows:
                print("Nanoparticle ID: {}; Elements: {}; Description: {}".format(row[0], row[2], row[1]))
                print(row[-1])
        else:
            query = "SELECT id, Description, Elements FROM Nanoparticle"
            rows = self.sql_h.query(query)
            for row in rows:
                print("INCAR ID: {}; Elements: {}; Description: {}".format(row[0], row[2], row[1]))

    def get_np(self, id):
        query = "SELECT Coordinates FROM Nanoparticle WHERE id="+str(id)
        return self.sql_h.query(query)[0][0]

    #######################################################
    # QM tasks
    #######################################################

    def set_potcar(self, potcar):
        with open(potcar, 'r') as f:
            self.qm.set_potcar(potcar=f.read())

    def generate_cluster(self, num, molecule=("", ), directory=None, np_id=None, shuffle=False, lattice=20,
                         lattice_scaling=1.0, centering=False, selective_dynamics=True,
                         potcars=None):

        # making sure that incar and kpoints are chosen
        # potcar file is checked later
        assert self.incar_id, "Please set the incar_id according to the INCAR database"
        assert self.kpoints_id, "Please set the kpoints_id according to the INCAR database"

        # checking and creating correpsonding directories
        if directory is not None:
            if os.path.exists(directory):
                if os.path.exists(directory+"_moved"):
                    os.removedirs(directory+"_moved")
                shutil.move(directory, directory+"_moved")
            os.mkdir(directory)

        # checking multiple adsorption states
        if type(molecule) is str: molecule = (molecule, )
        if len(molecule) > 1:
            assert len(molecule) == len(potcars), "A list of POTCARs is needed for the various adsorption states"
            poscars_temp = []
            for p in potcars:
                with open(p, 'r') as f:
                    poscars_temp.append(f.read())
            potcars = tuple(poscars_temp)
        else:
            potcars = (self.qm.potcar)

        # joining various SQL where clauses together
        where = []
        for m in molecule:
            where.append("ss.ID NOT IN (SELECT SurfaceID FROM {})".format('Cluster'+m))
        where = " AND ".join(where)
        if np_id is not None:
            where += " AND ss.NP_ID=" + str(np_id)
        if where: where = "WHERE " + where

        # getting the clusters from the SQL database
        clusters = self.sql_h.query(
            "SELECT ss.ID, ss.NP_ID, ss.natoms, ss.Rcut, ss.Elements, ss.ElementList, ss.Coordinates FROM SurfaceSites ss " + where)
        if shuffle: random.shuffle(clusters)
        clusters = clusters[:num]

        # craeting VASP input directory for each cluster
        for c in clusters:
            dictionary = {"SurfaceID": c[0], "NP_ID": c[1], "natoms": c[2], "Rcut": c[3],
                          "Elements": c[4], "KPOINTS_ID": self.kpoints_id, "INCAR_ID": self.incar_id}
            if directory is None:
                dir = "Cluster" + str(c[0])
            else:
                dir = directory + "/Cluster" + str(c[0])
            element_list = c[5].split(' ')
            coordinates = c[6]
            for i, m in enumerate(molecule):
                poscar = self.qm.generate_poscar(coordinates=coordinates, elements=element_list,
                                                 lattice=lattice, lattice_scaling=lattice_scaling,
                                                 centering=centering, selective_dynamics=selective_dynamics,
                                                 molecule=m)
                self.qm.generate_vasp(poscar=poscar, directory=dir+m, potcar=potcars[i],
                                      info={**dictionary, **{"molecule": m}})


    #######################################################
    # INCAR database
    #######################################################

    def add_incar(self, filename, Description=None):
        with open(filename, 'r') as f:
            incar = f.read()
        self.sql_h.insert("INSERT INTO INCAR VALUES (%s, %s, %s)", (None, Description, incar))
        pass

    def show_incar(self, id=None):
        if id is not None:
            query = "SELECT id, Description, Text FROM INCAR WHERE id="+str(id)
            rows = self.sql_h.query(query)
            for row in rows:
                print("INCAR ID: {}; Description: {}".format(row[0], row[1]))
                print(row[2])
        else:
            query = "SELECT id, Description FROM INCAR"
            rows = self.sql_h.query(query)
            for row in rows:
                print("INCAR ID: {}; Description: {}".format(row[0], row[1]))

    def get_incar(self, id):
        query = "SELECT Text FROM INCAR WHERE id="+str(id)
        return self.sql_h.query(query)[0][0]

    def use_incar(self, id):
        self.incar_id = id
        incar = self.sql_h.query("SELECT Text FROM INCAR WHERE id="+str(id))[0][0]
        self.qm.set_incar(incar=incar)

    #######################################################
    # KPOINTS database
    #######################################################

    def add_kpoints(self, filename, Description=None):
        with open(filename, 'r') as f:
            incar = f.read()
        self.sql_h.insert("INSERT INTO KPOINTS VALUES (%s, %s, %s)", (None, Description, incar))
        pass

    def show_kpoints(self, id=None):
        if id is not None:
            query = "SELECT id, Description, Text FROM KPOINTS WHERE id="+str(id)
            rows = self.sql_h.query(query)
            for row in rows:
                print("KPOINTS ID: {}; Description: {}".format(row[0], row[1]))
                print(row[2])
        else:
            query = "SELECT id, Description FROM KPOINTS"
            rows = self.sql_h.query(query)
            for row in rows:
                print("KPOINTS ID: {}; Description: {}".format(row[0], row[1]))

    def get_kpoints(self, id):
        query = "SELECT Text FROM KPOINTS WHERE id="+str(id)
        return self.sql_h.query(query)[0][0]

    def use_kpoints(self, id):
        self.kpoints_id = id
        kpoints = self.sql_h.query("SELECT Text FROM KPOINTS WHERE id="+str(id))[0][0]
        self.qm.set_kpoints(kpoints=kpoints)