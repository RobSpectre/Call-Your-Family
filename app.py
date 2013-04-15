import os

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

from twilio import twiml
from twilio.util import TwilioCapability


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')


@app.route('/', methods=['GET', 'POST'])
def index():
    # Make sure we have this host configured properly.
    config_errors = []
    for option in ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN']:
        if not app.config[option]:
            config_errors.append("%s is not configured for this host."
                    % option)

    # Define important links
    params = {
        'sms_request_url': url_for('.sms', _external=True),
        'config_errors': config_errors}

    # Generate capability token
    capability = TwilioCapability(app.config['TWILIO_ACCOUNT_SID'],
        app.config['TWILIO_AUTH_TOKEN'])
    capability.allow_client_outgoing(app.config['TWILIO_APP_SID'])
    token = capability.generate()

    # If not a submission, render form.
    return render_template('index.html', params=params, token=token)


@app.route('/voice', methods=['POST'])
def voice():
    response = twiml.Response()
    with response.dial() as dial:
        dial.number(request.form['PhoneNumber'])
    return str(response)


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    # Respond to any text inbound text message with a link to the app!
    response = twiml.Response()
    response.sms("This number belongs to the Twilio Call Your Family app for " \
            "Boston.  Please visit [URL] for more info.")
    return str(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
