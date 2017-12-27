# tests/handlers/test_api.py
import unittest
import json

from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

from swap import server


class TestBase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

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


class ApiHandlerTest(TestBase):

    def setUp(self):
        super(ApiHandlerTest, self).setUp()
        self.testbed.init_datastore_v3_stub()

    def testAuthorized(self):
        # Not authorized
        response = self.app.get('/item/')
        self.assertEqual(response.status_code, 401)

        # Authorized
        self.loginUser()
        response = self.app.get('/item/')
        self.assertEqual(response.status_code, 200)

    def testGet(self):
        self.loginUser(id='1')
        # No items
        response = self.app.get('/item/')
        json_data = json.loads(response.data)
        self.assertTrue('result' in json.loads(response.data))
        self.assertEqual(json_data['result'], [])

        # Add one item
        response = self.app.post('/item/', data='test')
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('result' in json_data)
        item_id = json_data['result']

        # Get items
        response = self.app.get('/item/')
        json_data = json.loads(response.data)
        self.assertTrue('result' in json_data)
        result = json_data['result']
        self.assertEqual(len(result), 1)
        item, = result
        self.assertEqual(item['description'], 'test')
        self.assertEqual(item['id'], item_id)

        # Get items for other user
        self.loginUser(id='2')
        response = self.app.get('/item/')
        json_data = json.loads(response.data)
        self.assertEqual(json_data['result'], [])

    def testGetOther(self):
        self.loginUser(id='1')
        response = self.app.post('/item/', data='test')
        response = self.app.get('/item/?owner=2')
        json_data = json.loads(response.data)
        self.assertEqual(json_data['result'], [])

        # this items should be visible to another
        self.loginUser(id='2')
        response = self.app.get('/item/?owner=1')
        json_data = json.loads(response.data)
        self.assertEqual(json_data['result'][0]['description'], 'test')


class ApiHandlerTest2(TestBase):
    def setUp(self):
        super(ApiHandlerTest2, self).setUp()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=1)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

    def testSwap(self):

        # Create items
        self.loginUser(id='1')
        response = self.app.post('/item/', data='item1')
        item_1 = json.loads(response.data)['result']

        self.loginUser(id='2')
        response = self.app.post('/item/', data='item2')
        item_2 = json.loads(response.data)['result']

        response = self.app.post('/swapping/', data=json.dumps(
            {'my': item_2, 'other': item_1}))
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/item/')
        json_data = json.loads(response.data)
        self.assertEqual(json_data['result'][0]['id'], item_1)

    def testSwapCheat(self):
        # Create items
        self.loginUser(id='1')
        response = self.app.post('/item/', data='item1')
        item_1 = json.loads(response.data)['result']

        self.loginUser(id='2')
        response = self.app.post('/item/', data='item2')
        item_2 = json.loads(response.data)['result']

        # Tring to swap not my item
        response = self.app.post('/swapping/', data=json.dumps({'my': item_1, 'other': item_2}), content_type='application/json',)
        self.assertEqual(response.status_code, 400)
