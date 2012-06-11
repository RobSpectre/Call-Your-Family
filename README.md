# Mobile App Distribution with SMS 

An example Flask application demonstrating how to invite users to download your
mobile application using Twilio SMS.

Built for Rob's talk on mobile app distribution originally given at USV, June
2012.

[![Build
Status](https://secure.travis-ci.org/RobSpectre/Mobile-App-Distribution-with-SMS)]
(http://travis-ci.org/RobSpectre/Mobile-App-Distribution-with-SMS)


## Summary

This is a quick Flask app I put together to demonstrate a common Twilio use
case, using SMS to invite users to download your mobile application.  100% of
your mobile app customers can receive SMS and with its naturally simple, 160
character interface and easy implementation using Twilio, it makes an effective,
cheap and very easy way to get your app in front of potential users.

This app is an example of this use case with two components.

1. A simple web form that will send a link to the app to the to the submitted
   phone number.
1. An SMS Request URL that will respond to incoming texts with a link to the
   app.

App used in the live example is for my favorite iPhone game, Plants vs. Zombies.


## Usage

Text anything to (646) 606-2920 to see it work!

![Example of it
working](https://raw.github.com/RobSpectre/Mobile-App-Distribution-with-SMS/master/images/usage.png)


## Installation

Step-by-step on how to deploy and develop this app.

### Deploy 

1) Grab latest source
<pre>
git clone git://github.com/RobSpectre/Mobile-App-Distribution-with-SMS.git 
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

6) Configure a new TwiML app and Twilio phone number to use the app.
<pre>
python configure.py --account_sid ACxxxxxx --auth_token yyyyyyy -n -N
</pre>

7) Text the new number and roll your next character!


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

Took the liberty of including some simple tests for the examples here.  Easy for
you to expand on for your use case.

<pre>
make test
</pre>


## Meta 

* No warranty expressed or implied.  Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by [Twilio New
 York](http://www.meetup.com/Twilio/New-York-NY/) 
