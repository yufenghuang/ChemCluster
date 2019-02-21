import unittest
from chemcluster.sql import SQLHandler

class TestSQLConnection(unittest.TestCase):

    def setUp(self):
        self.sql_h = SQLHandler()

    def test_connection(self):
        self.sql_h.connect("sql_config.ini")

    def test_query(self):
        results = self.sql_h.query("SELECT * FROM books")
        for result in results:
            print(result)

    def tearDown(self):
        self.sql_h.disconnect()

if __name__ == '__main__':
    unittest.main()