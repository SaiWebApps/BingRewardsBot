import argparse
import getpass

from bot.botconfig import PhantomJSBotConfig
from bot.manager import BingRewardsBotManager
from bot.account_manager.credentials import sqlliteprocessor

def get_credentials(filename, email_addresses):
    if not email_addresses:
        return sqlliteprocessor.process_credentials(filename)
    email_address_list = email_addresses.split(',')
    password_list = [getpass.getpass('Password for ' + email + ': ') for email in email_address_list]
    passwords = ','.join(password_list)
    return sqlliteprocessor.save_credentials(filename, email_addresses, passwords)

def main():
    # Extract target Bing Rewards accounts' credentials from the specified JSON file.
    parser = argparse.ArgumentParser(description = 'Accumulate daily Bing Rewards desktop and mobile points.')
    parser.add_argument('-f', '--filename', required = True, \
        help = 'Name of JSON file with Bing Rewards account credentials;' + \
               'if it does not exist, specify alongside "-e" to create.')
    parser.add_argument('-e', '--email_addresses', required = False, \
        help = 'Comma-separated Bing Rewards accounts\' email addresses;' + \
                'will be added to credentials JSON file if it already exists' + \
                'but will create and add to a new JSON file if it doesn\'t.')
    args = parser.parse_args()
    creds = get_credentials(args.filename, args.email_addresses)

    # Perform searches.
    desktop_bot_config = PhantomJSBotConfig(30)
    mobile_bot_config = PhantomJSBotConfig(20)
    mgr = BingRewardsBotManager(desktop_bot_config, mobile_bot_config)
    mgr.execute(creds, creds)

if __name__ == '__main__':
    main()