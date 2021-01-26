from DataBasePY import config
import unittest
from unittest.mock import Mock 

class TestDataBaseConfig(unittest.TestCase):


    def testGetFileNamePRD(self):

        env = Mock()
        env.get.return_value = "prd"
        expected = "database_production.ini"
        actual = config.getFileName(env)
        self.assertEqual(expected, actual)

    def testGetFileNameElse(self):
        env = Mock()
        env.get.return_value = ";laj"
        expected = "database.ini"
        actual = config.getFileName(env)
        self.assertEqual(expected, actual)    