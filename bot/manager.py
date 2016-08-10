from desktop import DesktopBingRewardsBot
from mobile import MobileBingRewardsBot

# Thread Pools
class BingRewardsBotManager:
    def __init__(self, desktop_bot_config, mobile_bot_config):
        '''
            @description
            Constructor that creates a BingRewardsBotManager with the specified desktop 
            and mobile bot configuration.

            @param desktop_bot_config
            (Required) BotConfig instance for desktop.

            @param mobile_bot_config
            (Required) BotConfig instance for mobile.
        '''
        self.desktop_bot_config = desktop_bot_config
        self.mobile_bot_config = mobile_bot_config

    def execute(self, desktop_accounts, mobile_accounts):
        '''
            @description
            Automate Bing searches, and accumulate Bing Rewards points for the given
            collection of desktop and mobile accounts.

            @param desktop_accounts
            (Required) AccountCredentialsCollection for desktop

            @param mobile_accounts
            (Required) AccountCredentialsCollection for mobile
        '''
        bots = [DesktopBingRewardsBot(self.desktop_bot_config, account_credentials) \
            for account_credentials in desktop_accounts.credentials_collection]
        bots.extend([MobileBingRewardsBot(self.mobile_bot_config, account_credentials) \
            for account_credentials in mobile_accounts.credentials_collection])
        for bot in bots:
            bot.start()