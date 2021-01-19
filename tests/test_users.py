"""
This module tests the api running in whichever environment the BUILD_URL function is set.
In development this is local. Requests are made to 127.0.0.1:8080/api/ [endpoint]
"""
import unittest
import requests
from helpers import build_url


def common_setUpClass(cls):
    """
    setUpClass isolates classname and creates corresponding objects from
    the API
    """
    cls.cls_name = str(cls).split(('.'))[1][8:-2].lower()
    cls_name = cls.cls_name
    cls.test_obj = []
    for i in range(3):
        print(i)
        n = str(i)
        try:
            data = {
                'name': f'test{cls_name}Name',
                'handle': f'test{cls_name}Handle{n}'
            }
            if cls_name == 'users':
                data['email'] = f'test{cls_name}Email{n}'
                data['password'] = f'niceTry'
            response = requests.post(build_url(f'api/{cls_name}'), data=data).json()
            print(f'api/{cls_name}')
            print('response = ', response)
            cls.test_obj.append(response.get(f'{cls_name}'))
        except Exception as e:
            print('API Failure *****')
            print(e)
    print('in setUp ', cls.test_obj)
    return cls.test_obj

def common_tearDownClass(cls, test_obj):
    # find one object with id, then delete actual object
    test_obj_one = test_obj[0]
    test_obj_two = test_obj[1]
    test_obj_three = test_obj[2]
    cls_name = cls.cls_name
    obj_ids = [test_obj_one.get('id'), test_obj_two.get('id'), test_obj_three.get('id')]
    cls_name_cap = cls_name.capitalize()[:-1]
    exec(f'from models.{cls_name} import {cls_name_cap}')
    for obj_id in obj_ids:
        exec(f'{cls_name_cap}.delete_from_db_with_id("{obj_id}")')
    print('in common_tearDown ', test_obj)
    




class TestAPI_Users(unittest.TestCase):
    """
    Test classes inheriting from TestApi_Users will test the API routes that
    correspond to their respective classname. Ex: TestAPI_Collectivess will test
    routes beginning with '/collectives'.
    """
    @classmethod
    def setUpClass(cls):
        cls.test_obj = common_setUpClass(cls)
        print('test object here', cls.test_obj)
    @classmethod
    def tearDownClass(cls):
        print('in outer tearDown', cls.test_obj)
        common_tearDownClass(cls, cls.test_obj)
    def test_some(self):
        pass


    """
    # post
    # check objects created have correct attributes
    # get
    # get all objects
    /users
    # get n objects
    /users/n
    # get all objects by attr/value
    /users/attr/value
    # get n objects by att/value
    /users/attr/value/n
    # update
    # update all objects
    /users
    # update all objects with attr to = value or put value in attr if iterable
    /users/attr/value
    # delete
    # delete one object by id
    /users/id
    # delete value from object with attr = value or value in attr
    users/attr/value
    """