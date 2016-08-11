from threading import Thread

from account_manager.browser_automation_utils.browser import AttributeType, Browser
from account_manager.desktop import DesktopAccountManager
from randomwordgenerator import randomwordgenerator

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

        # True if done executing, False otherwise
        self.done = False

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
            'unable_to_read_current': current == -1,
            'unable_to_read_maximum': maximum == -1,
            'read_both': current != -1 and maximum != -1
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
            # We're done, so update "done" status variable.
            self.done = True