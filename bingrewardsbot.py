from bingrewardsaccount import DesktopAccountManager, MobileAccountManager
from browser.browser import AttributeType, Browser
from randomwordgenerator import randomwordgenerator

class DesktopBingRewardsBot:
    def __init__(self, browser_type, sleep_between_searches = 5):
        '''
            @param browser_type
                (Required)
                BrowserType enum value specifying the type of browser that
                the user wants to utilize for search automation & points 
                accumulation

            @param sleep_between_searches
                (Optional)
                Numerical value specifying the delay between searches in seconds
        '''
        self.sleep_time = sleep_between_searches
        # Open the specified browser.
        self._init_account_manager(browser_type)

    def _init_account_manager(self, browser_type):
        '''
            @description
                Initialize the specified desktop browser, and pass the browser
                reference to a DesktopAccountManager for further handling.

            @param browser_type
                (Required)
                BrowserType enum value specifying the type of browser that
                the user wants to utilize for search automation & points 
                accumulation
        '''
        self.browser = Browser(browser_type = browser_type, mobile = False)
        self.account_manager = DesktopAccountManager(self.browser)

    def _perform_random_searches(self, num_searches):
        '''
            @description
                Perform the specified number of Bing searches, if
                we can still accumulate points for the day.
                In the worst-case, if we can't load any stats for the
                given account, then we will still perform the specified 
                number of searches. But we cannot guarantee the accumulation
                of the appropriate number of points.

            @param num_searches
                (Required) 
                Integer number of Bing searches that the user wants to automate.
        '''
        # Total lifetime number of points
        daily_device_points = self.account_manager.get_daily_device_points()
        # Number of points accumulated today
        current_device_points = daily_device_points[0]
        # Maximum number of points that can be accumulated today
        max_device_points = daily_device_points[1]
        # Should be >= max_device_points
        target_device_points = current_device_points + int(num_searches / 2)

        self.browser.open('http://www.bing.com')

        current_num_retries = 0
        MAX_NUM_RETRIES = 5

        while current_device_points < target_device_points:
            # Exit loop if we've already accumulated the maximum possible 
            # number of points for the day.
            if current_device_points >= max_device_points:
                break

            # If we can't read the current number of points or the maximum
            # possible number of points, then increment the number of retries.
            if current_device_points == 0 or max_device_points == 0:
                current_num_retries = current_num_retries + 1
            # If we've hit the maximum number of retries, then break.
            if current_num_retries >= MAX_NUM_RETRIES:
            	break

            # Normal Case: Generate "num_searches" random words, and perform
            # a Bing search using each term. Wait N seconds between searches,
            # so that Bing can't detect their automated nature.
            random_queries = randomwordgenerator.generate_random_words(num_searches)
            for query in random_queries:
                self.browser.type_and_submit(AttributeType.Name, 'q', query, clear_after_submit = True)
                self.browser.sleep(self.sleep_time)

            # Try to read/capture the number of points accumulated today.
            current_device_points = self.account_manager.get_daily_device_points()[0]

        self.account_manager.open_dashboard()

    def _safe_perform_random_searches(self, num_searches):
        '''
            @description
                Wrapper function around _perform_random_searches.
                Catches any exceptions and prints out the account stats.
                In the worst-case scenario, we can't find the search box,
                so we don't perform any searches.

            @param num_searches
                (Required)
                Integer number of Bing searches that the user wants to automate.
        '''
        try:
            self._perform_random_searches(num_searches)
        except:
            pass
        finally:
            print(self.account_manager)

    def execute(self, account_credentials, num_searches):
        '''
            @description
                For the given user account, automate the specified
                number of Bing searches and accumulate the apposite
                number of points.
                Note that we are using the same browser window across
                all accounts.

            @param account_credentials
                (Required) 
                User's Hotmail/Outlook email address & password; 
                needed to accumulate points under this user's account

            @param num_searches
                (Required) 
                Number of Bing searches that user with given
                credentials wants to automate.
        '''
        for creds in account_credentials:
            self.account_manager.account_creds = creds
            self.account_manager.sign_in()
            self._safe_perform_random_searches(num_searches)
            self.account_manager.sign_out()

    def finish(self):
        '''
            @description
                Close the browser, and release all resources.
        '''
        self.browser.close()
        self.browser = None

class MobileBingRewardsBot(DesktopBingRewardsBot):
    def _init_account_manager(self, browser_type):
        '''
            @description
                DesktopBingRewardsBot used a single account manager (and browser window)
                across all accounts.
                However, this bot will open a new browser window for each account, so
                we will merely store the browser type and create a manager at the outset.
        '''
        self.browser_type = browser_type
        self.account_manager = MobileAccountManager()

    def execute(self, account_credentials, num_searches):
        '''
            @description
                Unlike DesktopBingRewardsBot, this bot will create a new account manager,
                thereby creating a new browser window, for each given account.
                Otherwise, the functionality is identical.
        '''
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