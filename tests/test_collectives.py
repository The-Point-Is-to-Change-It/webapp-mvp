import unittest
import requests
from helpers import build_url
from tests.test_users import Base_Test


class TestAPI_Collectives(Base_Test, unittest.TestCase):
    """
    Test classes inheriting from TestApi_Users will test the API routes that
    correspond to their respective classname. Ex: TestAPI_Collectivess will test
    routes beginning with '/collectives'.
    """
    def test_a(self):
        pass
    def test_b(self):
        pass


