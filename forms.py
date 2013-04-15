import re

from wtforms import Form
from wtforms import TextField
from wtforms import validators
from wtforms import ValidationError


class NoCharacters(object):
    def __init__(self, message=None):
        if not message:
            message = u'Must be a phone number - no alpha characters.'
        self.message = message

    def __call__(self, form, field):
        p = re.compile('[a-z]', re.IGNORECASE)
        if p.search(field.data):
            raise ValidationError(self.message)


class PhoneNumberValidationForm(Form):
    phone_number = TextField('Enter Your Phone Number', [validators.Required(),
        validators.length(min=7, max=25), NoCharacters()])

    @property
    def e164(self):
        # Simple number scrubbing for demo purposes. Obvious US bias.
        e164_number = filter(lambda x: x in u'0123456789+',
                self.phone_number.data)
        if len(e164_number) == 10:
            e164_number = u'+1' + e164_number
        if e164_number[0] != u'+':
            e164_number = u'+' + e164_number
        return e164_number
