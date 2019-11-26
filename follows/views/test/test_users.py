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

    def test_login_required_unfollow(self):
        reply = self.client.post('unfollow', json={"user_id": 1})
        self.assertEqual(reply.status_code, 404)

        reply = self.client.post('unfollow', json={"user_id": 1, "followee_id": 1})
        self.assertEqual(reply.status_code, 404)
        self.assert_template_used("message.html")

    def test_login_required_my_followers(self):
        reply = self.client.get('/my_wall/followers')
        self.assertEqual(reply.status_code, 404)

        reply = self.client.get('/my_wall/followers')
        self.assertEqual(reply.status_code, 404)
        self.assert_template_used("myfollowers.html")

    def test_nonexistant_public_wall(self):
        reply = self.client.get('/wall/2')
        self.assertEqual(reply.status_code, 404)
        self.assert_template_used("message.html")

    # FIXME 
    def test_follow_unfollow_existing_user(self):   
        
        reply = self.client.get('/wall/1/follow')
        self.assertEqual(reply.status_code, 404)
        self.assert_template_used("message.html")

        reply = self.client.get('/wall/1/follow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")

        reply = self.client.get('/wall/1/unfollow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")

        reply = self.client.get('/wall/1/unfollow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")