import os

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect

from twilio import twiml
from twilio.rest import TwilioRestClient


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')


'''
Index Page
Show a simple web form to submit your phone number and receive an
SMS message.
'''
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if this is a submitted form, if so send the submitted
        # phone number an SMS invite.
        client = TwilioRestClient(app.config['ACCOUNT_SID'],
            app.config['AUTH_TOKEN'])
        client.sms.messages.create(from_=app.config['TWILIO_ACCOUNT_SID'],
                to=request.form['phone_number'], body="Download Plants vs. "\
                        "Zombies now using this link: %s" % \
                        url_for('.invite', external=True))
        params = {
            'phone_number': request.form['phone_number']}
        return render_template('thankyou.html', params=params)
    else:
        # If this is a GET, display the form to send the SMS invite.
        params = {
            'invite_uri': url_for('.invite', external=True)}
        return render_template('index.html', params=params)


'''
Invite URI
This is the link users are set to redirect them to the app in their platform's
app store.
'''
@app.route('/invite')
def invite():
    # If user is on iPhone/iPad, send to iTunes App Store
    if "iOS" in request.useragent:
        return redirect(app.config['IOS_URI'])
    # If user is on Android, send to Google Marketplace
    elif "Android" in request.useragent:
        return redirect(app.config['ANDROID_URI'])
    # Anything else, given them the web experience
    else:
        return redirect("http://plantsvszombies.com")


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
