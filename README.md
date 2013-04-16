# Call Your Family 

A free Twilio app to let Boston residents call their families while phone
coverage is poor.

Built following the tragic loss of life during the Boston Marathon, 15 April
2013.

[![Build
Status](https://secure.travis-ci.org/RobSpectre/Call-Your-Family.png?branch=master)](http://travis-ci.org/RobSpectre/Call-Your-Family)

## Summary

Simple app using [Twilio Client](http://www.twilio.com/client) to let folks
affected by the tragedy at the Boston Marathon to call their family.

It works like this:

1. Put a phone number in the input box on the right.
1. Click call.
1. Click "Allow" on the permissions dialog that follows.
1. Speak into the microphone on your laptop or desktop to talk with your family for
up to ten minutes.


## Usage

Once you deploy this app, you get a simple web form that asks you to put in your
phone number:

![Call Form](https://raw.github.com/RobSpectre/Mobile-App-Distribution-with-SMS/master/static/images/screenshot1.png)

Call is then placed to the number (if it is valid) using Twilio Client.



## Installation

Step-by-step on how to deploy and develop this app.

### Deploy 

1) Grab latest source
<pre>
git clone git://github.com/RobSpectre/Call-Your-Family.git 
</pre>

2) Install dependencies
<pre>
make init
</pre>

3) Navigate to folder and create new Heroku Cedar app
<pre>
heroku create --stack cedar
</pre>

4) Deploy to Heroku
<pre>
git push heroku master
</pre>

5) Scale your dynos
<pre>
heroku scale web=1
</pre>

6) Configure Heroku to use your Twilio credentials.
<pre>
python configure.py --account_sid ACxxxxxx --auth_token yyyyyyy
</pre>

7) Open the app in your browser and get an invite!
<pre>
heroku open
</pre> 


### Development

Be sure to follow the configuration steps above and use this step-by-step
guide to tweak to your heart's content.

1) Install the dependencies.
<pre>
make init
</pre>

2) Launch local development webserver
<pre>
foreman start
</pre>

3) Open browser to [http://localhost:5000](http://localhost:5000).

4) Tweak away on `app.py`.


## Testing

This example app comes with a full testing suite with the same kind of form
validation that you would want to use in production.  To run the tests, simply
use `nose` with this shortcut command:

<pre>
make test
</pre>


## Anatomy

This app does have a little more complexity than our usual examples in an effort
to be production-ready.  Here's a quick rundown of all the important files:

* `local_settings.py` - Contains all the configuration options for the app,
  including Twilio credentials and the URIs you want to which you wish to direct
  your mobile users.
* `app.py` - The meat of the app.  Contains all the logic for rendering the
  form, sending the invites, and redirecting mobile users.
* `tests` - Test suite testing the web, Twilio and form validation functionality
  of this example.
* `templates` - The gorgeous interface I surreptitiously from
  [Andres](http://twitter.com/enborra).
* `static` - Location of the styles for above.


## Meta 

* No warranty expressed or implied.  Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by [Twilio](http://www.twilio.com) 


Call your folks.  They'd like to hear from you.
