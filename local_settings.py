'''
Configuration Settings
'''

''' Uncomment to configure using the file.
WARNING: Be careful not to post your account credentials on GitHub.

TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "yyyyyyyyyyyyyyyy"
TWILIO_APP_SID = "APzzzzzzzzz"
TWILIO_CALLER_ID = "+17778889999"
IOS_URI = "http://phobos.apple.com/whatever"
ANDROID_URI = "http://market.google.com/somethingsomething"
'''

# Begin Heroku configuration - configured through environment variables.
import os
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', None)
TWILIO_CALLER_ID = os.environ.get('TWILIO_CALLER_ID', None)
TWILIO_APP_SID = os.environ.get('TWILIO_APP_SID', None)
IOS_URI = os.environ.get('IOS_URI',
    'http://itunes.apple.com/us/app/plants-vs.-zombies/id350642635?mt=8&uo=4')
ANDROID_URI = os.environ.get('ANDROID_URI',
        'http://market.android.com/details?id=com.popcap.pvz_row')
WEB_URI = os.environ.get('WEB_URI',
        'http://www.popcap.com/games/plants-vs-zombies/pc')
