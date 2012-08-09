import unittest

from werkzeug.datastructures import MultiDict

from .context import forms


class TestSmsInviteForm(unittest.TestCase):
    def test_e164(self):
        test_formats = ['(555) 555 5555', '555.555.5555', '(555)555.5555',
                '5555555555']
        for test_format in test_formats:
            test_form = forms.SMSInviteForm(MultiDict([('phone_number',
                test_format)]))
            self.assertTrue(test_form.e164 == "+15555555555",
                    "e164 formatting did work for %s, instead got: %s" %
                    (test_format, test_form.e164))

    def test_e164Negative(self):
        test_form = forms.SMSInviteForm(MultiDict([('phone_number',
            '+15555555555')]))
        self.assertTrue(test_form.e164 == '+15555555555', 'Form reformatted ' \
                'a number already in e.164: %s' % test_form.e164)

    def test_characterValidation(self):
        test_formats = ['(asd)555-5555', 'asdf555_555-5555', 'asd.555.5555']
        for test_format in test_formats:
            test_form = forms.SMSInviteForm(MultiDict([('phone_number',
                test_format)]))
            test_form.validate()
            self.assertTrue(test_form.errors, "SMSInviteForm validated the " \
                    "following invalid format: %s" % test_format)

    def test_characterValidationNegative(self):
        test_form = forms.SMSInviteForm(MultiDict([('phone_number',
            '+15555555555')]))
        self.assertFalse(test_form.errors, "SMSInviteForm invalidated the " \
                "following valid format: %s" % '+15555555555')
