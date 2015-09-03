import enum
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

# Currently, the supported browsers are Google Chrome, Firefox,
# Internet Explorer, and PhantomJS (headless).
# Please ensure that the former 3 are installed on your system
# before trying to load their webdrivers.
class BrowserType(enum.Enum):
    Firefox = 'firefox'
    Chrome = 'chrome'
    PhantomJS = 'phantomjs'

# Mobile browser user-agent string - allows desktop browser to pretend to be a mobile browser
# First User-Agent = Android browser; works for Firefox and Chrome webdrivers
_MOBILE_BROWSER_USER_AGENT = 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; ' + \
    'LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 ' + \
    ' Mobile Safari/534.30'
# Second User-Agent = IPad/IPhone browser; works for PhantomJS webdriver
_MOBILE_BROWSER_USER_AGENT2 = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) ' + \
    'AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'

# WebDriver Abstract Class
class WebDriver:
    def __init__(self, exec_path, mobile=False):
        '''
            @param exec_path
                (Required) The path to the target webdriver executable
                for this platform.

            @param mobile
                (Optional; False by default) Specifies whether or not
                this webdriver should spoof a mobile user-agent string.
        '''
        self.exec_path = exec_path
        self.mobile = mobile

    def get_driver(self):
        pass

# Prerequisite: Firefox must be installed on your system.
class FirefoxDriver(WebDriver):
    def __init__(self, exec_path, mobile=False):
        # Selenium offers built-in support for the Firefox driver,
        # so no exec_path is necessary.
        super().__init__(None, mobile)

    def get_driver(self):
        '''
            @return a Selenium Firefox web driver object; if the
                "mobile" option was specified, configure the object
                to spoof a mobile browser's user-agent string.
        '''
        profile = webdriver.FirefoxProfile()
        if self.mobile:
            profile.set_preference('general.useragent.override', _MOBILE_BROWSER_USER_AGENT)
        return webdriver.Firefox(profile)

# Prerequisite: Google Chrome must be installed on your system.
class ChromeDriver(WebDriver):
    def __init__(self, exec_path, mobile=False):
        super().__init__(exec_path, mobile)

    def get_driver(self):
        executable_path = self.exec_path
        opts = Options()
        if self.mobile:
            opts.add_argument('user-agent=' + _MOBILE_BROWSER_USER_AGENT)
        return webdriver.Chrome(self.exec_path, chrome_options = opts)

# Headless
class PhantomJSDriver(WebDriver):
    def __init__(self, exec_path, mobile=False):
        super().__init__(exec_path, mobile)

    def get_driver(self):
        capabilities = dict(DesiredCapabilities.PHANTOMJS)
        if self.mobile:
            capabilities['phantomjs.page.settings.userAgent'] = _MOBILE_BROWSER_USER_AGENT2
        return webdriver.PhantomJS(self.exec_path, service_log_path = os.devnull, \
            desired_capabilities = capabilities)

# Other constants - used for webdriver configuration
SELENIUM_WEBDRIVER = 'webdriver'
CURRENT_PLATFORM = sys.platform.lower()

# Map BrowserType to collection of webdriver executable paths.
WEBDRIVER_CONFIG = {
    BrowserType.Firefox.value: {
        SELENIUM_WEBDRIVER: FirefoxDriver
    },
    BrowserType.Chrome.value: {
        SELENIUM_WEBDRIVER: ChromeDriver,
        'win32': 'webdrivers/chromedriver.exe',
        'linux': 'webdrivers/chromedriver'
    },
    BrowserType.PhantomJS.value: {
        SELENIUM_WEBDRIVER: PhantomJSDriver,
        'win32': 'webdrivers/phantomjsdriver.exe',
    }
}
