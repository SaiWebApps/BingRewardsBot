import argparse

from bingrewardsbot import BotConfig, BingRewardsBotManager
from browser.webdrivermanager.browsertypes import BrowserType
from credentialsprocessor import process_credentials

def main():
	# Extract target Bing Rewards accounts' credentials from the specified JSON file.
	parser = argparse.ArgumentParser(description = 'Meet daily Bing Rewards desktop and mobile search quota.')
	parser.add_argument('-f', '--filename', required = True, help = 'Name of JSON file with Bing Rewards account credentials')
	args = parser.parse_args()	
	creds = credentials_processor.process_credentials(args.filename)

	# Perform searches.
	desktop_bot_config = BotConfig(BrowserType.PhantomJS, 30)
	mobile_bot_config = BotConfig(BrowserType.PhantomJS, 20)
	mgr = BingRewardsBotManager(desktop_bot_config, mobile_bot_config)
	mgr.execute(creds, creds)

if __name__ == '__main__':
    main()
