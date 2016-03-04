from threading import Thread

from browser.browser import AttributeType, Browser
from bingrewardsaccount import DesktopAccountManager, MobileAccountManager
from randomwordgenerator import randomwordgenerator

class BotConfig:
    def __init__(self, browser_type, num_searches, sleep_time_between_searches = 5):
        '''
            @param browser_type
            (Required, browser.webdrivermanager.browsertypes.BrowserType)
            Type of the browser that is going to automate Bing searches.

            @param num_searches
            (Required, int)
            Number of Bing searches that will be automated.

            @param sleep_time_between_searches
            (Optional, Default Value = 5, int)
            Number of seconds of delay between Bing searches.
            Tricks Bing servers into thinking that human is performing searches, so
            that we can accumulate points.
        '''
        self.browser_type = browser_type
        self.num_searches = num_searches
        self.sleep_time_between_searches = sleep_time_between_searches

# Threads - 1:1 relationship between threads/bots and Bing-Rewards-Accounts
class DesktopBingRewardsBot(Thread):
    def __init__(self, bot_config, account_credentials):
        '''
            @param bot_config
            Meta-configuration parameters for this desktop bot.

            @param account_credentials
            (Required, bingrewardsaccount.AccountCredentials)
            Credentials for Bing Rewards account that this thread is 
            accumulating points for.
        '''
        super().__init__()

        # Save parameters.
        self.browser_type = bot_config.browser_type
        self.num_searches = bot_config.num_searches
        self.sleep_time_between_searches = bot_config.sleep_time_between_searches
        self.account_credentials = account_credentials

        # Vars to be defined later
        self.browser = None
        self.account_manager = None

    def initialize(self):
        '''
            @description
            Open a new browser window, and pass the reference to a new Bing Rewards
            account manager.
        '''
        self.browser = Browser(self.browser_type)
        self.account_manager = DesktopAccountManager(self.browser, self.account_credentials)

    def release(self):
        '''
            @description
            If this thread has opened a browser window, then close it.
        '''
        if self.browser:
            self.browser.close()

    def _execute_random_searches(self):
        # Normal Case: Generate "num_searches" random words, and perform
        # a Bing search using each term. Wait N seconds between searches,
        # so that Bing can't detect their automated nature.
        random_queries = randomwordgenerator.generate_random_words(self.num_searches)
        for query in random_queries:
            self.browser.type_and_submit(AttributeType.Name, 'q', query, \
                clear_after_submit = True)
            self.browser.sleep(self.sleep_time_between_searches)
    
    def _unable_to_read_points(self, current, target, maximum):
        return current == 0 or target == 0 or maximum == 0

    def perform_random_searches(self):
        '''
            @description
                Perform the specified number of Bing searches, if we can still
                accumulate points for the day.
                In the worst-case, if we can't load any stats for the given account,
                then we will still perform the specified number of searches. But, in
                such a case, we can't guarantee the accumulation of the appropriate 
                number of points.
        '''
        # Total lifetime number of points
        daily_device_points = self.account_manager.get_daily_device_points()
        # Number of points accumulated today
        current_device_points = daily_device_points[0]
        # Maximum number of points that can be accumulated today
        max_device_points = daily_device_points[1]
        # Should be >= max_device_points
        target_device_points = current_device_points + int(self.num_searches / 2)

        self.browser.open('http://www.bing.com')

        current_num_retries = 0
        MAX_NUM_RETRIES = 5

        while current_device_points < target_device_points and target_device_points < max_device_points and \
                current_num_retries < MAX_NUM_RETRIES:
            # If we can't read the current number of points or the maximum
            # possible number of points, then increment the number of retries.
            if self._unable_to_read_points(current_device_points, target_device_points, max_device_points):
                current_num_retries = current_num_retries + 1

            self._execute_random_searches()

            # Try to read/capture the number of points accumulated today.
            current_device_points = self.account_manager.get_daily_device_points()[0]

        if self._unable_to_read_points(current_device_points, target_device_points, max_device_points):
            self._execute_random_searches()
        self.account_manager.open_dashboard()

    def run(self):
        try:
            self.initialize()
            self.account_manager.sign_in()
            self.perform_random_searches()
            self.account_manager.accumulate_special_offer_points()
            print(self.account_manager)
            self.account_manager.sign_out()
        finally:
            self.release()

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

# Thread Pools
class BingRewardsBotManager:
    def __init__(self, desktop_bot_config, mobile_bot_config):
        '''
            @description
            Constructor that creates a BingRewardsBotManager with the specified desktop and mobile
            bot configuration.

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
        bots = [DesktopBingRewardsBot(self.desktop_bot_config, account_credentials) for account_credentials in desktop_accounts.credentials_collection]
        bots.extend([MobileBingRewardsBot(self.mobile_bot_config, account_credentials) for account_credentials in mobile_accounts.credentials_collection])
        for bot in bots:
            bot.start()