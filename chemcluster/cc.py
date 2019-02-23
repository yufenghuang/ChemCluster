from .sql import SQLHandler
from .np import Nanoparticle

class CC:
    '''
        This is the main object to perform tasks on ChemCluster
    '''

    sql_h = SQLHandler()
    nanoparticle = Nanoparticle()

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
        clusters = self.nanoparticle.get_clusters(element, Rcut=Rcut)
        self.sql_h.insert("INSERT INTO Nanoparticles VALUES (%s, %s, %s)", (None, description, self.nanoparticle.to_xyz()))

    def show_np(self, id=None):
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

    def get_np(self, id):
        query = "SELECT Coordinates FROM Nanoparticle WHERE id="+str(id)
        return self.sql_h.query(query)[0][0]

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

    #######################################################
    # QM tasks
    #######################################################

    def add_qm(self, database):
        pass

    def show_qm(self, database):
        pass

    def print_qm(self, database, index):
        pass