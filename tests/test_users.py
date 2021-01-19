"""
This module tests the api running in whichever environment the BUILD_URL function is set.
In development this is local. Requests are made to 127.0.0.1:8080/api/ [endpoint]
"""
import unittest
import requests
from helpers import build_url


class Base_Test():
    @classmethod
    def setUpClass(cls):
        """
        setUpClass isolates classname and creates corresponding objects from
        the API
        """
        cls.cls_name = str(cls).split(('.'))[1][8:-2].lower()
        cls_name = cls.cls_name
        cls.test_obj = []
        for i in range(3):
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
                print(response, '*********')
                cls.test_obj.append(response.get(f'{cls_name}'))
            except Exception as e:
                print('API Failure *****')
                print(e)

    @classmethod
    def tearDownClass(cls):
        # find one object with id, then delete actual object
        test_obj_one = cls.test_obj[0]
        test_obj_two = cls.test_obj[1]
        test_obj_three = cls.test_obj[2]
        cls_name = cls.cls_name
        obj_ids = [test_obj_one.get('id'), test_obj_two.get('id'), test_obj_three.get('id')]
        cls_name_cap = cls_name.capitalize()[:-1]
        exec(f'from models.{cls_name} import {cls_name_cap}')
        for obj_id in obj_ids:
            exec(f'{cls_name_cap}.delete_from_db_with_id("{obj_id}")')

    @classmethod
    def get_test_objects(cls):
        return (cls.test_obj[0], cls.test_obj[1], cls.test_obj[2], cls.cls_name)

    def test_create(self):
        obj_1, obj_2, obj_3, cls_name = self.__class__.get_test_objects()
        self.assertEqual(obj_1.get('handle'), f'test{cls_name}Handle0')
    
    def test_get_all(self):
        obj_1, obj_2, obj_3, cls_name = self.__class__.get_test_objects()
        response = requests.get(build_url(f'api/{cls_name}')).json()
        self.assertEqual(response.get('status'), 'OK')
    def test_get_n(self):
        obj_1, obj_2, obj_3, cls_name = self.__class__.get_test_objects()
        response = requests.get(build_url(f'api/{cls_name}/2')).json()
        self.assertEqual(response.get('status'), 'OK')
        self.assertEqual(len(response.get(f'{cls_name}')), 2)
    def test_get_all_by_attr_value(self):
        obj_1, obj_2, obj_3, cls_name = self.__class__.get_test_objects()
        response = requests.get(build_url(f'api/{cls_name}/name/test{cls_name}Name')).json()
        self.assertEqual(response.get('status'), 'OK')
        self.assertEqual(len(response.get(f'{cls_name}')), 3)
    def common_get_n_by_attr_value(self):
        pass
    def common_update_all(self):
        pass
    def common_update_by_attr_value(self):
        pass
    def common_delete_by_id(self):
        pass
    def common_delete_value_from_attr(self):
        pass
        




class TestAPI_Users(Base_Test, unittest.TestCase):
    """
    Test classes inheriting from TestApi_Users will test the API routes that
    correspond to their respective classname. Ex: TestAPI_Collectivess will test
    routes beginning with '/collectives'.
    """
    pass
    
   
   