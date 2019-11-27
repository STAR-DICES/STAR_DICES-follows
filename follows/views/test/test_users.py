import unittest
import json

from follows.app import start
from flask_testing import TestCase


class TestAuth(TestCase):
    def create_app(self):
        self.app = start(test=True)
        self.context = self.app.app_context()
        self.client = self.app.test_client()
        return self.app

    def tearDown(self):
        self.app = None
        self.context = None
        self.client = None

    def test_wrong_parameters_follow(self):
        data = {
            'user_id': 1,
            'followee_id': 2
        }
        r = self.client.post('/follow', json=data)
        self.assertEqual(r.status_code, 400)

    def test_wrong_parameters_unfollow(self):
        data = {
            'followee_id': 2
        }
        r = self.client.delete('/follow', json=data)
        self.assertEqual(r.status_code, 400)

    def test_double_follow(self):
        data = {
            'user_id': 2,
            'followee_id': 1,
            'user_name': 'Admin'
        }
        r = self.client.post('/follow', json=data)
        self.assertEqual(r.status_code, 409)

    def test_nonexistant_unfollow(self):
        data = {
            'user_id': 10,
            'followee_id': 11,
        }
        r = self.client.delete('/follow', json=data)
        self.assertEqual(r.status_code, 409)

    def test_self_follow(self):
        data = {
            'user_id': 10,
            'followee_id': 10,
            'user_name': 'test'
        }
        r = self.client.post('/follow', json=data)
        self.assertEqual(r.status_code, 401)

    def test_self_unfollow(self):
        data = {
            'user_id': 10,
            'followee_id': 10,
        }
        r = self.client.delete('/follow', json=data)
        self.assertEqual(r.status_code, 401)

