from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error

class SQLHandler:
    """
        The class to communicate with the SQL database
    """

    # sql connction
    conn = MySQLConnection()

    def __init__(self, filename=''):
        # connect to SQL
        if filename:
            self.connect(filename)

    def connect(self, filename):
        '''
        Establish a connection to the database using the information in the config file
        :param filename: path_to_the_location_of_the_config_file
        :return: None
        '''
        db_config = read_db_config(filename)
        try:
            self.conn = MySQLConnection(**db_config)
            if not self.conn.is_connected():
                raise Exception('Cannot connect to database using the config file {}'.format(filename))
        except Error as error:
            print(error)

    def disconnect(self):
        if self.conn.is_connected():
            self.conn.close()

    def is_connected(self):
        return self.conn.is_connected()

    def query(self, sql_query):
        """
        Execute a query command on the sql server, and the resutls are returned in a list
        :param sql_query: SQL query
        :return: list consisting of rows matching the SQL query
        """
        assert self.conn.is_connected(), "Connection needs to be established before query"
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        cursor.close()
        return [row for row in rows]

    def execute(self, sql_query):
        """
        Execute a query command on the sql server, no results are returned
        :param sql_query:
        :return: None
        """
        assert self.conn.is_connected(), "Connection needs to be established before query"
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        cursor.close()

    def insert(self, sql_query, values):
        """
        Insert values on the sql server, no results are returned
        :param sql_query:
        :return: None
        """
        assert self.conn.is_connected(), "Connection needs to be established before query"
        cursor = self.conn.cursor()
        cursor.execute(sql_query, values)
        self.conn.commit()
        cursor.close()

    def insertmany(self, sql_query, values):
        """
        Insert a list of values on the sql server, no results are returned
        :param sql_query:
        :return: None
        """
        assert self.conn.is_connected(), "Connection needs to be established before query"
        cursor = self.conn.cursor()
        cursor.executemany(sql_query, values)
        self.conn.commit()
        cursor.close()

def read_db_config(filename):
    '''
    Read the parameters from sql_config file. The format of the config file is follows:
        [mysql]
        host = host_address
        database = dabase_name
        user = user_name
        password = pass_word
    :param filename: path_to_the_location_of_the_config_file
    :return: the items to establish a sql connection
    '''
    parser = ConfigParser()
    parser.read(filename)

    db = {}

    if parser.has_section("mysql"):
        items = parser.items("mysql")
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('section [mysql] not found in the config file {}'.format(filename))

    return db