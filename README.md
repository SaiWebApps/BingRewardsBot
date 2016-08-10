# Bing Rewards Bot
<img src="http://www.casinoaffiliateprograms.com/blog/wp-content/uploads/2012/04/bingbot.jpg" />
<br><I> This bot is on the hunt. </I>

## Overview
#### What is Bing Rewards?
To incentivize more people to use Bing for web/mobile searches, Bing sponsors a loyalty program called Bing Rewards, which rewards users with points in return for signing in with a Hotmail/Outlook account and searching on Bing. Like the points in a frequent-flyer program, these points can be exchanged for gift cards and other amenities.
You can find out more about Bing Rewards <a href="http://www.bing.com/explore/rewards-g?FORM=MM0AQY&PUBL=GOOGLE&CREA=MM0AQY&ef_id=VX4fUwAAAFCA2Zp7:20150615004155:s">here</a>.

#### What is the purpose of this application?
<u>In 3 words - Automate Bing searches.</u> <br>
To accumulate Bing Rewards points, one must perform 30 desktop-based and 20 mobile-based Bing searches per day; this will yield a total of 25 Bing Rewards points per day. <br>
Now, for those who prefer non-Bing search engines (i.e, Google, DuckDuckGo), this could be difficult, whether due to forgetfulness or habit. So, this script will allow them to easily accumulate those points on days where they've neglected to perform the necessary amount of Bing searches.

## Prerequisites
* Python 3.5 or above
* randomwordgenerator-0.2
* requests
* selenium
* sqlalchemy

To install the latter 4 dependencies, run the following in the root/main directory:
```
pip install -r "requirements.txt"
```

## Supported Browsers
### WINDOWS

|         | Firefox   | Chrome    | Headless (PhantomJS) |
| ------- | --------- | --------- | -------------------- |
| Desktop | &#9745;   | &#9745;   | &#9745;              |
| Mobile  | &#9745;   | &#9745;   | &#9745;              |

### LINUX
|         | Firefox   | Headless (PhantomJS) |
| ------- | --------- | -------------------- |
| Desktop | &#9745;   | &#9745;              |
| Mobile  | &#9745;   | &#9745;              |

## Usage
usage: driver.py [-h] -f FILENAME [-e EMAIL_ADDRESSES]

Accumulate daily Bing Rewards desktop and mobile points.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Name of JSON file with Bing Rewards account
                        credentials; if it does not exist, specify alongside
                        "-e" to create.
  -e EMAIL_ADDRESSES, --email_addresses EMAIL_ADDRESSES
                        Comma-separated Bing Rewards accounts' email
                        addresses; will be added to credentials JSON file if
                        it already exists but will create and add to a new
                        JSON file if it doesn't.

If the "-e" flag is specified, driver.py will prompt for a password for each of the provided email accounts.
The given email addresses and passwords will then either be appended to the specified JSON file name if it already exists or written to a new JSON file with the given filename if it doesn't.

## TODO
* ~~For each account, display list of points before and after searches to confirm script's success.~~
* ~~Accumulate points successfully on Windows for Firefox, Chrome, and Headless/PhantomJS browsers.~~
* ~~Accumulate special offer points.~~
* ~~Multi-threading - Execute {account 1, account 2, etc.} searches in parallel.~~
* ~~Pass in account credentials to driver.py via command-line (raw-args, JSON/XML file, etc.).~~
* ~~Encrypt passwords in JSON file(s) created by credentialsprocessor module.~~
* ~~Implement SQL-lite credentials processing alternative to the JSON credentials processor.~~
* Create GUI for adding and saving account credentials.