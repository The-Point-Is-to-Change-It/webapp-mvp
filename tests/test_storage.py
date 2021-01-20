import unittest
from models.storage import storage
from models.base import Base
class TestStorage(unittest.TestCase):
    # POST METHODS
    def test_data_cycle(self):
        # save_obj_to_db
        try:
            base = Base(**{'testKey': 'testValue'})
            base.save_to_db()
        except Exception as e:
            self.assertEqual(e, None)
        test_obj_list = storage.get_n_by_cls_and_attr(Base, 'testKey', 'testValue', 1)
        self.assertTrue(type(test_obj_list) == list)
        self.assertTrue(len(test_obj_list) > 0)
        test_obj = test_obj_list[0]
        test_id = test_obj.get('id')
        self.assertTrue(type(test_obj) == dict)
        self.assertTrue(test_obj.get('testKey') == 'testValue')
        # delete_from_db_with_id
        storage.delete_from_db_with_id(Base, test_id)
        no_obj = storage.get_n_by_cls_and_attr(Base, 'testKey', 'testValue', 1)
        self.assertTrue(no_obj == [])
        # save_obj_to_db_with_dict
        try:
            storage.save_obj_to_db_with_dict('Base', test_obj)
        except Exception as e:
            self.assertEqual(e, None)
        test_obj_list = storage.get_n_by_cls_and_attr(Base, 'testKey', 'testValue', 1)
        self.assertTrue(type(test_obj_list) == list)
        self.assertTrue(len(test_obj_list) > 0)
        test_obj = test_obj_list[0]
        test_id = test_obj.get('id')
        self.assertTrue(type(test_obj) == dict)
        self.assertTrue(test_obj.get('testKey') == 'testValue')
        storage.delete_from_db_with_id(Base, test_id)
        no_obj = storage.get_n_by_cls_and_attr(Base, 'testKey', 'testValue', 1)
        self.assertTrue(no_obj == [])
        class Test():
            def __init__(self):
                pass
        all_test_objects = storage.get_all(Test)
        self.assertTrue(len(all_test_objects) == 3)
        two_test_objects = storage.get_n(Test, 2)
        self.assertTrue(len(two_test_objects) == 2)
        # get_n_by_cls_and_attr
        one_test_obj_by_attr = storage.get_n_by_cls_and_attr(Test, 'testKey', 'testValue', 1)
        self.assertTrue(len(one_test_obj_by_attr) == 1)
        storage.update_attr_by_id(Test, '265ywwRIC987OLiH9X0x', 'testKey', 'newValue')
        one_test_obj_by_attr = storage.get_n_by_cls_and_attr(Test, 'id', '265ywwRIC987OLiH9X0x', 1)
        self.assertTrue(one_test_obj_by_attr[0].get('testKey') == 'newValue')
        storage.update_attr_by_id(Test, '265ywwRIC987OLiH9X0x', 'testKey', 'testValue')
        one_test_obj_by_attr = storage.get_n_by_cls_and_attr(Test, 'id', '265ywwRIC987OLiH9X0x', 1)
        self.assertTrue(one_test_obj_by_attr[0].get('testKey') == 'testValue')
        
    
