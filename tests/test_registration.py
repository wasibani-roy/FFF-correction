import unittest
from fast_food_app import create_app
from flask import current_app as app
import json
from fast_food_app.database import Database
# from .test_data import *
user = {"username":"deo", "email":"deo@me.com", "password":"deo"}
user_admin_reg = {"username":"admin", "email":"admin@me.com", "password":"admin"}
user_log = {"username":"deo", "password":"deo"}
user_admin = {"username":"admin", "password":"admin"}
status_update = {"orderid":"1", "status":"pending"}
status_update_invalid = {"orderid":"1", "status":""}
class BaseCase(unittest.TestCase):
    """class holds all the unittests for the endpoints"""

    def setUp(self):
        """
            This method is run at the begining of each test
            also initialises the client where tests will be run

        """
        # user = {"username":"peter", "email":"peter@me.com", "password":"peter"}
        config_name = 'testing'
        self.app = create_app(config_name)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = Database(app.config['DATABASE_URL'])
        # self.db.create_tables()
        self.client = self.app.test_client()

    def create_valid_user(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/signup/',
                                    data=json.dumps(user),
                                    content_type='application/json')
        return response

    def create_admin_user(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/signup/',
                                    data=json.dumps(user_admin_reg),
                                    content_type='application/json')
        return response

    def get_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/login',
                                    data=json.dumps(user_log),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return 'Bearer ' + data['Access token']

    def get_admin_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/login',
                                    data=json.dumps(user_admin),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return 'Bearer ' + data['Access token']

    # def post_menu(self):
    #     """method for posting a menu """
    #     response = self.client.post(
    #         'api/v1/menu', data=json.dumps(menu), content_type='application/json', headers={'Authorization':
    #                                                                                             self.get_token()})
    #     return response

    # def place_an_order(self):
    #     """method for posting a menu """
    #     response = self.client.post(
    #         'api/v1/users/orders', data=json.dumps(order), content_type='application/json', headers={'Authorization':
    #                                                                                                      self.get_token()})
    #     return response

    def test_user_resgistration(self):
        response = self.create_valid_user()
        self.assertEqual(response.status_code, 201)
        # self.assertIn('you have succesfully signed up', str(response.data))

    def test_user_login(self):
        """method for testing user_login endpoint"""
        self.create_valid_user()
        response = self.client.post(
            '/api/v2/login/', data=json.dumps(user_log), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print(response.data)
        data = json.loads(response.data.decode())
        self.assertTrue(data['Access token'])

    def test_user_login_invalid_password(self):
        """method for testing user_login endpoint"""
        user_log2 = {"username":"deo", "password":"deo1"}
        self.create_valid_user()
        response = self.client.post(
            '/api/v2/login/', data=json.dumps(user_log2), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Invalid username and password', str(response.data))

    def test_user_login_invalid_username(self):
        """method for testing user_login endpoint"""
        user_log2 = {"username":"deot", "password":"deo1"}
        self.create_valid_user()
        response = self.client.post(
            '/api/v2/login/', data=json.dumps(user_log2), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('No user Found', str(response.data))

    def test_place_a_food_items_unauthorised(self):
        menu = {"product":"burger","description":"chicken burger", "price":"12000"}
        self.create_valid_user()
        response = self.client.post('api/v2/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 404)
        self.assertIn("Unauthorised", str(response.data))

    def test_place_a_food_items_authorised(self):
        menu = {"product":"burger","description":"chicken burger", "price":"12000"}
        self.create_admin_user()
        response = self.client.post('api/v2/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Menu item now created", str(response.data))

    def test_place_a_food_items_invalid_data(self):
        menu = {"description":"chicken burger", "price":"12000"}
        self.create_admin_user()
        response = self.client.post('api/v2/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 400)
        # self.assertIn("Menu item now created", str(response.data))

    def test_making_an_order(self):
        menu = {"product": "burger", "description": "chicken burger", "price": "12000"}
        self.create_admin_user()
        self.client.post('api/v2/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        order = {"menuid":"1"}
        self.create_valid_user()
        response = self.client.post('api/v2/order', data=json.dumps(order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 200)
        self.assertIn("order placed", str(response.data))

    def test_making_an_order_by_id(self):
        menu = {"product": "burger", "description": "chicken burger", "price": "12000"}
        self.create_admin_user()
        self.client.post('api/v2/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        order = {"menuid":"1"}
        self.create_valid_user()
        self.client.post('api/v2/order', data=json.dumps(order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        response = self.client.get('api/v2/order/1', content_type='application/json', headers={'Authorization':
                                             self.get_admin_token()})
        self.assertEqual(response.status_code, 200)
        # self.assertIn("You have not selected you're order", str(response.data))

    def test_making_an_order_by_id_not_admin(self):
        menu = {"product": "burger", "description": "chicken burger", "price": "12000"}
        self.create_admin_user()
        self.client.post('api/v2/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        order = {"menuid":"1"}
        self.create_valid_user()
        self.client.post('api/v2/order', data=json.dumps(order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        response = self.client.get('api/v2/order/1', content_type='application/json', headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 400)
        # self.assertIn("You have not selected you're order", str(response.data))

    def test_updating_an_order(self):
        menu = {"product": "burger", "description": "chicken burger", "price": "12000"}
        self.create_admin_user()
        self.client.post('api/v2/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        order = {"menuid":"1"}
        self.create_valid_user()
        self.client.post('api/v2/order', data=json.dumps(order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        response = self.client.put('api/v2/order/', data=json.dumps(status_update), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)
        # self.assertIn("You have not selected you're order", str(response.data))

    def test_updating_an_order_invalid(self):
        menu = {"product": "burger", "description": "chicken burger", "price": "12000"}
        self.create_admin_user()
        self.client.post('api/v2/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        order = {"menuid":"1"}
        self.create_valid_user()
        self.client.post('api/v2/order', data=json.dumps(order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        response = self.client.put('api/v2/order/', data=json.dumps(status_update_invalid), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 404)
        self.assertIn("Missing order id or order status", str(response.data))

    def tearDown(self):
        """method for rearing down the tables whenever a test is completed"""
        print('------Tearingdown----------------------')
        self.db.drop_table('users', 'menu', 'orders')