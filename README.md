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
* <a href="https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi">Python 3.4</a>
* requests, selenium - After installing python, you can install these via "pip install -r requirements.txt". We strongly recommend executing this command and installing these modules within a Python virtual environment (virtualenv).

## Supported Browsers
### WINDOWS

|         | Firefox   | Chrome    | Headless (PhantomJS) |
| ------- | --------- | --------- | -------------------- |
| Desktop | &#9745;   | &#9745;   | &#9745;              |
| Mobile  | &#9745;   | &#9745;   | &#9745;              |

### LINUX
|         | Firefox   | Chrome    | Headless (PhantomJS) |
| ------- | --------- | --------- | -------------------- |
| Desktop | &#9745;   |           | &#9745;              |
| Mobile  | &#9745;   |           | &#9745;              |

## Usage
usage: driver.py [-h] -f FILENAME

Meet daily Bing Rewards desktop and mobile search quota.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Name of JSON file with Bing Rewards account
                        credentials

### To create the JSON file ###
usage: credentialsprocessor.py [-h] [-f FILENAME] [-e EMAIL_ADDRESSES]
                               [-p PASSWORDS]

Process Bing-Rewards accounts' credentials

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Name of the JSON file that the credentials are/will be
                        stored in.
  -e EMAIL_ADDRESSES, --email_addresses EMAIL_ADDRESSES
                        Comma-separated list of email addresses.
  -p PASSWORDS, --passwords PASSWORDS
                        Comma-separated list of passwords corresponding to
                        each email address specified with "-e".

### Example Credentials JSON file ###
credentials.json

```json
[
	{
		"email" : "EMAIL1",
		"password": "PASSWORD1"
	},
	{
		"email" : "EMAIL2",
		"password": "PASSWORD2"
	},
	....
]
```

## TODO
* ~~For each account, display list of points before and after searches to confirm script's success.~~
* ~~Accumulate points successfully on Windows for Firefox, Chrome, and Headless/PhantomJS browsers.~~
* ~~Accumulate special offer points.~~
* ~~Multi-threading - Execute {account 1, account 2, etc.} searches in parallel.~~
* ~~Pass in account credentials to driver.py via command-line (raw-args, JSON/XML file, etc.).~~
* Encrypt passwords in JSON file(s) created by credentialsprocessor module.
* Create GUI for adding and saving account credentials.