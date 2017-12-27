# tests/handlers/test_api.py
import unittest
import json

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from swap import server


class ApiHandlerTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.app = server.get_app().test_client()
        ndb.get_context().clear_cache()

    def loginUser(self, email='user@example.com', id='123', is_admin=False):
        self.testbed.setup_env(
            user_email=email,
            user_id=id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)

    def tearDown(self):
        self.testbed.deactivate()

    def testGet(self):
        # Not authorized
        response = self.app.get('/item/')
        self.assertEqual(response.status_code, 301)

        # Authorized
        self.loginUser()
        response = self.app.get('/item/')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        self.assertEqual(json_data, [])
