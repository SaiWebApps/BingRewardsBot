from bingrewardsaccount import DesktopAccountManager, MobileAccountManager
from browser.browser import AttributeType, Browser
from randomwordgenerator import randomwordgenerator

class DesktopBingRewardsBot:
    def __init__(self, browser_type, sleep_between_searches = 5):
        '''
            @param browser_type
                BrowserType enum value specifying the type of browser that
                the user wants to utilize for search automation + points accumulation
        '''
        self.sleep_time = sleep_between_searches
        self._init_account_manager(browser_type)

    def _init_account_manager(self, browser_type):
        self.browser = Browser(browser_type = browser_type, mobile = False)
        self.account_manager = DesktopAccountManager(self.browser)

    def finish(self):
        '''
            Close the browser, and release all resources.
        '''
        if self.browser.browser:
            self.browser.close()
        self.browser = None

    def _perform_random_searches(self, num_searches):
        '''
            @param num_searches
                (Required) Number of Bing searches that the user wants to automate.
        '''
        daily_device_points = self.account_manager.get_daily_device_points()
        current_device_points = daily_device_points[0]
        max_device_points = daily_device_points[1]
        target_device_points = current_device_points + int(num_searches / 2)

        self.browser.open('http://www.bing.com')

        current_num_retries = 0
        MAX_NUM_RETRIES = 5

        while current_device_points < target_device_points:
            if current_device_points >= max_device_points:
                break
            if current_device_points == 0 or max_device_points == 0:
                current_num_retries = current_num_retries + 1
            if current_num_retries >= MAX_NUM_RETRIES:
            	break
            random_queries = randomwordgenerator.generate_random_words(num_searches)
            for query in random_queries:
                self.browser.type_and_submit(AttributeType.Name, 'q', query, clear_after_submit = True)
                self.browser.sleep(self.sleep_time)
            current_device_points = self.account_manager.get_daily_device_points()[0]

        self.account_manager.open_dashboard()

    def _safe_perform_random_searches(self, num_searches):
        try:
            self._perform_random_searches(num_searches)
        except:
            pass
        finally:
            print(self.account_manager)

    def execute(self, account_credentials, num_searches):
        '''
            @param account_credentials
                (Required) User's Hotmail/Outlook email address & password; 
                needed to accumulate points under this user's account

            @param num_searches
                (Required) Number of Bing searches that user with given
                credentials wants to automate.
        '''
        for creds in account_credentials:
            self.account_manager.account_creds = creds
            self.account_manager.sign_in()
            self._safe_perform_random_searches(num_searches)
            self.account_manager.sign_out()

class MobileBingRewardsBot(DesktopBingRewardsBot):
    def _init_account_manager(self, browser_type):
        self.browser_type = browser_type
        self.account_manager = MobileAccountManager()

    def execute(self, account_credentials, num_searches):
        for creds in account_credentials:
            # Open new browser window.
            self.account_manager.browser = Browser(browser_type = self.browser_type, mobile = True)
            self.browser = self.account_manager.browser

            # Sign in, perform searches, and accumulate points.
            self.account_manager.account_creds = creds
            self.account_manager.sign_in()
            self._safe_perform_random_searches(num_searches)

            # Close browser window.
            self.browser.close()