import enum
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

_MOBILE_BROWSER_USER_AGENT = 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; ' + \
	'LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'

class BrowserType(enum.Enum):
	Firefox = 'firefox'
	Chrome = 'chrome'
	IE = 'ie'
	PhantomJS = 'phantomjs'

class WebDriver:
	def __init__(self, exec_path, mobile=False):
		self.exec_path = exec_path
		self.mobile = mobile

	def get_driver(self):
		pass

class FirefoxDriver(WebDriver):
	def __init__(self, exec_path, mobile=False):
		super().__init__(None, mobile)

	def get_driver(self):
		profile = webdriver.FirefoxProfile()
		if self.mobile:
			profile.set_preference('general.useragent.override', _MOBILE_BROWSER_USER_AGENT)
		return webdriver.Firefox(profile)

class IeDriver(WebDriver):
	def __init__(self, exec_path, mobile=False):
		super().__init__(exec_path, mobile)

	def get_driver(self):
		caps = DesiredCapabilities.INTERNETEXPLORER
		caps['ignoreProtectedModeSettings'] = True
		return webdriver.Ie(self.exec_path, capabilities = caps)

class ChromeDriver(WebDriver):
	def __init__(self, exec_path, mobile=False):
		super().__init__(exec_path, mobile)

	def get_driver(self):
		chrome_driver = webdriver.Chrome
		executable_path = self.exec_path
		opts = Options()
		if self.mobile:
			opts.add_argument('user-agent=' + _MOBILE_BROWSER_USER_AGENT)
		return webdriver.Chrome(self.exec_path, chrome_options = opts)

class PhantomJSDriver(WebDriver):
	def __init__(self, exec_path, mobile=False):
		super().__init__(exec_path, mobile)

	def get_driver(self):
		return webdriver.PhantomJS(self.exec_path, service_log_path = os.devnull)

SELENIUM_WEBDRIVER = 'webdriver'
CURRENT_PLATFORM = sys.platform.lower()

WEBDRIVER_CONFIG = {
	BrowserType.Firefox.value: {
		SELENIUM_WEBDRIVER: FirefoxDriver
	},
	BrowserType.Chrome.value: {
		SELENIUM_WEBDRIVER: ChromeDriver,
		'win32': 'webdrivers/chromedriver.exe',
		'darwin': 'webdrivers/chromedriver.osx',
		'linux2': 'webdrivers/chromedriver'
	},
	BrowserType.IE.value: {
		SELENIUM_WEBDRIVER: IeDriver,
		'win32': 'webdrivers/iedriver.exe'
	},
	BrowserType.PhantomJS.value: {
		SELENIUM_WEBDRIVER: PhantomJSDriver,
		'win32': 'webdrivers/phantomjsdriver.exe',
		'darwin': 'webdrivers/phantomjsdriver.osx'
	}
}