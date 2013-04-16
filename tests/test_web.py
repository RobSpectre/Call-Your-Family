import unittest

from .context import app

app.config['TWILIO_ACCOUNT_SID'] = 'ACxxxxxx'
app.config['TWILIO_AUTH_TOKEN'] = 'yyyyyyyyy'
app.config['TWILIO_CALLER_ID'] = '+15558675309'
app.config['IOS_URI'] = \
    'http://itunes.apple.com/us/app/plants-vs.-zombies/id350642635?mt=8&uo=4'
app.config['ANDROID_URI'] = \
        'http://market.android.com/details?id=com.popcap.pvz_row'
app.config['WEB_URI'] = 'http://www.popcap.com/games/plants-vs-zombies/pc'


class WebTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


class IndexTests(WebTest):
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual("200 OK", response.status)
