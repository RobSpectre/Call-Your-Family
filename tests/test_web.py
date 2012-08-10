import unittest
from mock import patch

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
        self.assertTrue("/invite" in response.data,
                "Did not get invite URI in response: %s" % response.data)

    @patch('twilio.rest.resources.SmsMessages')
    @patch('twilio.rest.resources.SmsMessage')
    def test_invitePostGoodInput(self, MockMessage, MockMessages):
        app.twilio_client.sms.messages = MockMessages.return_value
        app.twilio_client.sms.messages.create.return_value = \
            MockMessage.return_value
        response = self.app.post('/',
                data={'phone_number': '555-555-5555'}, follow_redirects=True)
        self.assertEqual("200 OK", response.status)
        app.twilio_client.sms.messages.create.assert_called_once_with(
            from_=app.config['TWILIO_CALLER_ID'],
            to="+15555555555",
            body="Download Plants vs. Zombies now using this link: " \
                    "http://localhost/invite")

    @patch('twilio.rest.resources.SmsMessages')
    @patch('twilio.rest.resources.SmsMessage')
    def test_invitePostBadInput(self, MockMessage, MockMessages):
        app.twilio_client.sms.messages = MockMessages.return_value
        app.twilio_client.sms.messages.create.return_value = \
            MockMessage.return_value
        response = self.app.post('/',
                data={'phone_number': 'asdfasdfasdf'}, follow_redirects=True)
        self.assertEqual("200 OK", response.status)
        self.assertFalse(app.twilio_client.sms.messages.create.called,
                "SMS message sent with poor input: %s" % 'asdfasdfasdf')


class InviteTests(WebTest):
    def test_invite(self):
        response = self.app.get('/invite', headers=[
            ('User-Agent', 'Test Client')])
        print str(response.headers)
        self.assertEqual("302 FOUND", response.status)
        self.assertEqual(response.headers['Location'], app.config['WEB_URI'])

    def test_Android(self):
        response = self.app.get('/invite', headers=[
            ('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.0.1; en-us; sdk' \
                'Build/ICS_MR0) AppleWebKit/534.30 (KHTML, like Gecko)' \
                'Version/4.0 Mobile Safari/534.30 ')])
        self.assertEqual("302 FOUND", response.status)
        self.assertEqual(response.headers['Location'],
                app.config['ANDROID_URI'])

    def test_iOS(self):
        response = self.app.get('/invite', headers=[
            ('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like ' \
                    'Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) ' \
                    'Version/5.1 Mobile/9B176 Safari/7534.48.3`')])
        self.assertEqual("302 FOUND", response.status)
        self.assertEqual(response.headers['Location'], app.config['IOS_URI'])
