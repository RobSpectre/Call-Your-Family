import unittest
from .context import app

class WebTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


class InviteTests(WebTest):
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual("200 OK", response.status)
        self.assertTrue("/invite?external=True" in response.data,
                "Did not get invite URI in response: %s" % response.data)


    def test_inviteGetWeb(self):
        response = self.app.get('/invite')
        self.assertEqual("301 REDIRECT", response.status)
