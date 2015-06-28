import sys

from browser.webdrivermanager.browsertypes import BrowserType
from bingrewardsbotstrategy import BingDesktopStrategy, BingMobileStrategy

def main():
	# Enter Hotmail/Outlook creds here.
	creds = []
	for user in creds:
		strategy = BingDesktopStrategy(BrowserType.PhantomJS)
		strategy.execute(user['email'], user['password'], 30)
	for user in creds:
		strategy = BingMobileStrategy(BrowserType.PhantomJS)
		strategy.execute(user['email'], user['password'], 20)

if __name__ == '__main__':
	main()