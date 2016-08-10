from threading import Thread

from browser_automation_utils.browser import AttributeType, Browser
from bingrewardsaccount import DesktopAccountManager, MobileAccountManager
from random_word_generator import randomwordgenerator

class BotConfig:
    def __init__(self, browser_type, num_searches, sleep_time_between_searches = 5):
        '''
            @param browser_type
            (Required, browser_automation_utils.browsertypes.BrowserType)
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
    
    def _get_point_stats(self):
        '''
            @return
                A dictionary containing 4 key-value pairs:
                - 'current': The # of device points accumulated today
                - 'maximum': The maximum possible # of device points that can be accumulated today
                - 'unable_to_read_current': A boolean; if true, then can't read number of device points 
                accumulated today.
                - 'unable_to_read_maximum': A boolean; if true, then can't read maximum number of device
                points that can be accumulated today.
        '''
        daily_device_points = self.account_manager.get_daily_device_points()
        if not daily_device_points:
        	daily_device_points = [-1, -1]
        return {
            'current': daily_device_points[0],
            'maximum': daily_device_points[1],
            'unable_to_read_current': daily_device_points[0] == -1,
            'unable_to_read_maximum': daily_device_points[1] == -1,
            'read_both': daily_device_points[0] != -1 and daily_device_points[1] != -1
        }

    def _try_get_point_stats(self, num_retries = 1):
        current = -1
        maximum = -1

        for i in range(0, num_retries):
            device_point_stats = self._get_point_stats()
            # If we read both stats successfully, return dictionary immediately.
            if device_point_stats['read_both']:
                return device_point_stats

            # Salvage as much info as possible from current attempt.
            if not device_point_stats['unable_to_read_current']:
                current = device_point_stats['current']
            if not device_point_stats['unable_to_read_maximum']:
                maximum = device_point_stats['maximum']

        if maximum == -1:
            maximum = current + int(self.num_searches / 2)

        # At this point, we were not able to read at least 1 stat.
        # So, populate dictionary w/ what data we managed to gather, and compute booleans
        # based on gathered data.
        return {
            'current': current,
            'maximum': maximum,
            'unable_to_read_current': daily_device_points[0] == -1,
            'unable_to_read_maximum': daily_device_points[1] == -1,
            'read_both': daily_device_points[0] != -1 and daily_device_points[1] != -1
        }

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
        MAX_RETRIES = 5

        stats = self._try_get_point_stats(MAX_RETRIES)

        # Open Bing home page.
        self.browser.open('http://www.bing.com')

        # Perform the specified number of random searches until either the
        # current number of accumulated points exceeds the maximum possible
        # points for today, OR we've hit the retry ceiling.
        num_retries = 0
        while stats['current'] < stats['maximum'] and num_retries < MAX_RETRIES:
            self._execute_random_searches()
            stats = self._try_get_point_stats(MAX_RETRIES)
            if stats['unable_to_read_current']:
                num_retries = num_retries + 1

        self.account_manager.open_dashboard()

    def view_special_offers(self):
        offer_points = self.account_manager.get_daily_offer_points()
        (current, maximum) = (offer_points[0], offer_points[1])
        (current_num_retries, max_num_retries) = (0, 3)
        while current < maximum and current_num_retries < max_num_retries:
            self.account_manager.accumulate_special_offer_points()
            current_num_retries = current_num_retries + 1

    def run(self):
        try:
            self.initialize()
            self.account_manager.sign_in()
            self.perform_random_searches()
            self.view_special_offers()
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