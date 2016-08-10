from account_manager.browser_automation_utils.browser import Browser
from account_manager.mobile import MobileAccountManager
from desktop import DesktopBingRewardsBot

class MobileBingRewardsBot(DesktopBingRewardsBot):
    def __init__(self, bot_config, account_credentials):
        super().__init__(bot_config, account_credentials)

    def initialize(self):
        '''
            @description
            The only difference in this method-override is that we are using mobile,
            not desktop, resources. 
        '''
        self.browser = Browser(self.browser_type, mobile = True)
        self.account_manager = MobileAccountManager(self.browser, self.account_credentials)