from desktop import DesktopBingRewardsBot
from mobile import MobileBingRewardsBot

# Thread Pools
class BingRewardsBotManager:
    def __init__(self, desktop_bot_config, desktop_accounts, mobile_bot_config, mobile_accounts):
        '''
            @description
            Constructor that creates a set of desktop and mobile Bing Rewards 
            bots with the specified configurations and for the given accounts.

            @param desktop_bot_config
            (Required) BotConfig instance for desktop

            @param desktop_accounts
            (Required) AccountCredentialsCollection for desktop
            
            @param mobile_bot_config
            (Required) BotConfig instance for mobile

            @param mobile_accounts
            (Required) AccountCredentialsCollection for mobile
        '''
        self.bot_list = [DesktopBingRewardsBot(desktop_bot_config, account) \
            for account in desktop_accounts.credentials_collection]
        self.bot_list.extend([MobileBingRewardsBot(mobile_bot_config, account) \
            for account in mobile_accounts.credentials_collection])

    def run(self):
        '''
            @description
            Run the desktop and/or mobile Bing Rewards bots in bot_list.
        '''
        for bot in self.bot_list:
            bot.start()

    def count_finished_bots(self):
        '''
            @return
            The number of Bing Rewards bots that have finished executing.
        '''
        return sum([bot.done for bot in self.bot_list])

    def get_percent_completed(self):
        '''
            @return
            The percentage of bots in bot_list that have finished executing.
        '''
        return 100 * (self.count_finished_bots() / len(self.bot_list))