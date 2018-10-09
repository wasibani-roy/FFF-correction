import unittest
from fast_food_app import create_app
from flask import current_app as app
import json
from fast_food_app.database import Database
# from .test_data import *
user = {"username":"peter", "email":"peter@me.com", "password":"peter"}

class BaseCase(unittest.TestCase):
    """class holds all the unittests for the endpoints"""

    def setUp(self):
        """
            This method is run at the begining of each test
            also initialises the client where tests will be run

        """
        user = {"username":"peter", "email":"peter@me.com", "password":"peter"}
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



    def test_user_resgistration(self):
        response = self.create_valid_user()
        self.assertEqual(response.status_code, 201)
        # self.assertIn('you have succesfully signed up', str(response.data))

    def tearDown(self):
        """method for rearing down the tables whenever a test is completed"""
        print('------Tearingdown----------------------')
        self.db.drop_table('users')