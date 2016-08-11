from account_manager.browser_automation_utils.browsertypes import BrowserType

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

class PhantomJSBotConfig(BotConfig):
    '''
        Extension of BotConfig that uses headless/PhantomJS Selenium driver.
    '''
    def __init__(self, num_searches, sleep_time_between_searches = 5):
        super().__init__(BrowserType.PhantomJS, num_searches, sleep_time_between_searches)