import unittest
from mock import patch

from .context import app

app.config['TWILIO_ACCOUNT_SID'] = 'ACxxxxxx'
app.config['TWILIO_AUTH_TOKEN'] = 'yyyyyyyyy'
app.config['TWILIO_CALLER_ID'] = '+15558675309'

class WebTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


class InviteTests(WebTest):
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual("200 OK", response.status)
        self.assertTrue("/invite?external=True" in response.data,
                "Did not get invite URI in response: %s" % response.data)

    @patch('twilio.rest.resources.SmsMessages')
    @patch('twilio.rest.resources.SmsMessage')
    def test_invitePostGoodInput(self, MockMessage, MockMessages):
        app.twilio_client.sms.messages = MockMessages.return_value
        app.twilio_client.sms.messages.create = MockMessage.return_value
        response = self.app.post('/',
            data={'phone_number': '555-555-5555'})
        self.assertEqual("200 OK", response.status)
        app.twilio_client.sms.messages.create.assert_called_once_with(
            from_=app.config['TWILIO_CALLER_ID'],
            to="+15555555555",
            body="Download Plants vs. Zombies now using this link: " \
                "/invite?external=True")

    def test_invite(self):
        response = self.app.get('/invite')
        self.assertEqual("301 REDIRECT", response.status)

