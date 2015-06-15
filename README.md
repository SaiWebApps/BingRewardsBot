# Bing Rewards Bot
<img src="http://www.casinoaffiliateprograms.com/blog/wp-content/uploads/2012/04/bingbot.jpg" />
<br><I> This bot is on the hunt. </I>

## Overview
#### What is Bing Rewards?
To incentivize more people to use Bing for web/mobile searches, Bing sponsors a loyalty program called Bing Rewards, which rewards users with points in return for signing in with a Hotmail/Outlook account and searching on Bing. Like the points in a frequent-flyer program, these points can be exchanged for gift cards and other amenities.
You can find out more about Bing Rewards <a href="http://www.bing.com/explore/rewards-g?FORM=MM0AQY&PUBL=GOOGLE&CREA=MM0AQY&ef_id=VX4fUwAAAFCA2Zp7:20150615004155:s">here</a>.

#### What is the purpose of this application?
<u>In 3 words - Automate Bing searches.</u> <br>
To accumulate Bing Rewards points, one must perform 30 desktop-based and 20 mobile-based Bing searches; this will yield a total of 25 Bing Rewards points per day. <br>
Now, for those who prefer non-Bing search engines (i.e, Google, DuckDuckGo), this could be difficult, whether due to forgetfulness or habit. So, this script will allow them to easily accumulate those points on days where they've neglected to perform the necessary amount of Bing searches.

## Prerequisites
* A Windows, Linux, or Mac OSX desktop/laptop
* <a href="https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi">Python 3.4</a>
* requests, selenium - After installing python, you can install these via "pip install -r requirements.txt". We strongly recommend executing this command and installing these modules within a Python virtual environment (virtualenv).

## How To Execute
python bingrewardsbot.py

## TODO
* Add more comments.
* Read list of Hotmail/Outlook accounts from JSON and/or XML file rather than hard-coding them.
* For each account, display list of points before and after searches to confirm script's success.
* Schedule script to run at user-specified time every day.