# aliexpress-orders

I wanted a way to get all of my AliExpress parcel's tracking ID's
This script first grabs all of your orders from the overview and then visits every order detail site to grab the tracking ID.

Turns out you can only log in with JavaScript enabled.
Selenium takes care of that.

To run this you need selenium installed and chromedriver in your $PATH

`python3 -m pip install selenium`