from .sql import SQLHandler

class CC:
    '''
        This is the main object to perform tasks on ChemCluster
    '''

    sql_h = SQLHandler()

    def __init__(self, config_file=''):
        if config_file:
            self.sql_h = SQLHandler(config_file)

    def is_connected(self):
        return self.sql_h.is_connected()

    def connect(self, config_file):
        self.sql_h.connect(config_file)

    def disconnect(self):
        self.sql_h.disconnect()

    def add_np(self, xyzFile, description, remove=None):
        pass

    def show_np(self):
        # show the saved nanoparticles in the database
        pass

    def print_np(self, index):
        pass

    def add_incar(self, filename):
        with open(filename, 'r') as f:
            incar = f.read()
        self.sql_h.insert("INSERT INTO INCAR VALUES (%s, %s)", (None, incar))
        pass

    def show_incar(self, id = None):
        if id is not None:
            query = "SELECT Text FROM INCAR WHERE id="+str(id)
        else:
            query = "SELECT Text FROM INCAR"
        rows = self.sql_h.query(query)
        for row in rows:
            print(row[0])

    def add_kpoints(self, filename):
        with open(filename, 'r') as f:
            incar = f.read()
        self.sql_h.insert("INSERT INTO KPOINTS VALUES (%s, %s)", (None, incar))
        pass

    def show_kpoints(self):
        if id is not None:
            query = "SELECT Text FROM KPOINTS WHERE id="+str(id)
        else:
            query = "SELECT Text FROM KPOINTS"
        rows = self.sql_h.query(query)
        for row in rows:
            print(row[0])

    def show_databases(self):
        pass

    def add_qm(self, database):
        pass

    def show_qm(self, database):
        pass

    def print_qm(self, database, index):
        pass