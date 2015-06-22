import os

import browsertypes

_ABS_PATH_TO_THIS_DIR = os.path.realpath(os.path.dirname(__file__))

def _make_path_absolute(path):
	'''
		@param path
			A relative or absolute path to a webdriver executable __file__

		@return
			- If path is absolute or None, then return as is.
			- Otherwise, if path is relative, then make it absolute by prepending
			_ABS_PATH_TO_THIS_DIR to it.
	'''
	abs_path = path
	if not path or os.path.isabs(path):
		return path
	return os.path.join(_ABS_PATH_TO_THIS_DIR, path)

def get_selenium_webdriver(browser_type, mobile = False):
	'''
		@param browser_type
			Specifies the type of the target browser (e.g., Chrome, Firefox, etc.).

		@param mobile
			By default, mobile = False, so the webdriver will be returned as is,
			with no extra config.
			But, if mobile = True, then the webdriver will be configured to spoof
			a mobile browser's user-agent.
		
		@return
			- The Selenium webdriver object for the target browser type
			- None if no such object can be constructed (b/c of missing driver executable,
			missing config for specified browser type, etc.)
	'''
	all_webdriver_config = browsertypes.WEBDRIVER_CONFIG

	# If there is no webdriver config for the specified browser type, return None.
	driver_config = all_webdriver_config.get(browser_type.value, None)
	if not driver_config:
		return None

	# If the specified browser type is Firefox, then the executable path is not required
	# since Selenium offers in-built support for the Firefox webdriver.
	if browser_type == browsertypes.BrowserType.Firefox:
		return driver_config[browsertypes.SELENIUM_WEBDRIVER]

	# For all other browser types, get the path to the webdriver executable that can run
	# on the current platform, and create a Selenium webdriver object that uses this path.
	# If there is no path for the current platform, then return None.
	executable_path = _make_path_absolute(driver_config.get(browsertypes.CURRENT_PLATFORM, None))
	return driver_config[browsertypes.SELENIUM_WEBDRIVER](executable_path, mobile).get_driver() if executable_path else None
