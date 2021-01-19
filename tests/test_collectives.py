import unittest
import requests
from helpers import build_url
from tests.test_users import common_tearDownClass, common_setUpClass


class TestAPI_Collectives(unittest.TestCase):
    """
    Test classes inheriting from TestApi_Users will test the API routes that
    correspond to their respective classname. Ex: TestAPI_Collectivess will test
    routes beginning with '/collectives'.
    """
    @classmethod
    def setUpClass(cls):
        cls.test_obj = common_setUpClass(cls)
    @classmethod
    def tearDownClass(cls):
        common_tearDownClass(cls, cls.test_obj)
    def test_a(self):
        pass
    def test_b(self):
        pass


