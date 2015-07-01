import sys

from browser.webdrivermanager.browsertypes import BrowserType
from bingrewardsbotstrategy import BingDesktopStrategy, BingMobileStrategy

def main():
	# Enter Hotmail/Outlook creds here.
	creds = []
	for user in creds:
		desktop_strategy = BingDesktopStrategy(BrowserType.PhantomJS)
		desktop_strategy.execute(user['email'], user['password'], 30)
		mobile_strategy = BingMobileStrategy(BrowserType.PhantomJS)
		mobile_strategy.execute(user['email'], user['password'], 20)

if __name__ == '__main__':
	main()