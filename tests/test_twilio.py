import unittest
from .context import app


class TwiMLTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def assertTwiML(self, response):
        self.assertTrue("<Response>" in response.data, "Did not find " \
                "<Response>: %s" % response.data)
        self.assertTrue("</Response>" in response.data, "Did not find " \
                "</Response>: %s" % response.data)
        self.assertEqual("200 OK", response.status)

    def sms(self, body, path='/sms', number='+15555555555'):
        params = {
            'SmsSid': 'SMtesting',
            'AccountSid': 'ACtesting',
            'From': number,
            'To': '+16666666666',
            'Body': body,
            'ApiVersion': '2010-04-01',
            'Direction': 'inbound'}
        return self.app.post(path, data=params)

    def call(self, path='/voice', caller_id='+15555555555', digits=None,
            phone_number=None):
        params = {
            'CallSid': 'CAtesting',
            'AccountSid': 'ACtesting',
            'From': caller_id,
            'To': '+16666666666',
            'CallStatus': 'ringing',
            'ApiVersion': '2010-04-01',
            'Direction': 'inbound'}
        if digits:
            params['Digits'] = digits
        if phone_number:
            params['PhoneNumber'] = phone_number
        return self.app.post(path, data=params)


class TwilioTests(TwiMLTest):
    def test_voice(self):
        response = self.call(phone_number="+15557778888")
        self.assertTwiML(response)

    def test_inbound(self):
        response = self.call(path='/inbound')
        self.assertTwiML(response)

    def test_sms(self):
        response = self.sms("Test")
        self.assertTwiML(response)
