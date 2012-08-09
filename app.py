import os

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect

from twilio import twiml
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

from forms import SMSInviteForm

# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')
# Instantiate Twilio REST client to use for sending SMS.
if app.config['TWILIO_ACCOUNT_SID'] and app.config['TWILIO_AUTH_TOKEN']:
    app.twilio_client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'],
                app.config['TWILIO_AUTH_TOKEN'])


'''
Index Page
Show a simple web form to submit your phone number and receive an
SMS message.
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    # Make sure we have this host configured properly.
    config_errors = []
    for option in ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN']:
        if not app.config[option]:
            config_errors.append("%s is not configured for this host." % option)

    # Define important links
    params = {
        'sms_request_url': url_for('.sms', _external=True),
        'invite_uri': url_for('.invite', _external=True),
        'config_errors': config_errors}

    # Check if this is a submitted form, if so send the submitted
    # phone number an SMS invite.
    if request.method == 'POST':
        form = SMSInviteForm(request.form)
        # Check if form validates, if so send text message.
        if form.validate():
            try:
                app.twilio_client.sms.messages.create(
                    from_=app.config['TWILIO_CALLER_ID'],
                    to=form.e164, body="Download Plants vs. "\
                            "Zombies now using this link: %s" % \
                            url_for('.invite', _external=True))
            except TwilioRestException as e:
                # If we encounter a Twilio error, invalidate the form and
                # ask user to enter again.
                form.phone_number.errors = [unicode(e.msg)]
                return render_template('index.html', params=params,
                        form=form)
            # Render Thank You page.
            params = {
                'phone_number': request.form['phone_number']}
            return render_template('thankyou.html', params=params)
    else:
        # If it's not a post, just create a blank form.
        form = SMSInviteForm()

    # If not a submission, render form.
    return render_template('index.html', params=params, form=form)


'''
Invite URI
This is the link users are set to redirect them to the app in their platform's
app store.
'''


@app.route('/invite')
def invite():
    # Get user-agent
    user_agent = request.headers.get('User-Agent')
    # If user is on iPhone/iPad, send to iTunes App Store
    if "iPhone" in user_agent:
        return redirect(app.config['IOS_URI'])
    # If user is on Android, send to Google Marketplace
    elif "Android" in user_agent:
        return redirect(app.config['ANDROID_URI'])
    # Anything else, given them the web experience
    else:
        return redirect(app.config['WEB_URI'])


'''
SMS Request URL
This accepts incoming text messages and replies with a link to the app.
'''


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    response = twiml.Response()
    response.sms("Download Plants vs. Zombies now using this " \
            "link: %s" % url_for('.invite', external=True))
    return str(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
