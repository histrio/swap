# tests/handlers/test_api.py
import unittest
import json

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from handlers import api


class ApiHandlerTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.app = api.app.test_client()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def testPing(self):
        response = self.app.get('/api/v1.0/ping')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        self.assertEqual(json_data['ping'], 'pong')
