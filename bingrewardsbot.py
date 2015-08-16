from bingrewardsaccount import AccountCredentials, DesktopAccountManager, MobileAccountManager
from browser.browser import AttributeType, Browser
from browser.webdrivermanager.browsertypes import BrowserType
from randomwordgenerator import randomwordgenerator

class BingRewardsBot:
	def __init__(self, browser_type, is_mobile = False, sleep_between_searches = 5):
		'''
			@param browser_type
				BrowserType enum value specifying the type of browser that
				the user wants to utilize for search automation + points accumulation
		'''
		self.browser = Browser(browser_type = browser_type, mobile = is_mobile)
		self.account_manager = MobileAccountManager(self.browser) if is_mobile else DesktopAccountManager(self.browser)
		self.sleep_time = sleep_between_searches

	def finish(self):
		'''
			Close the browser, and release all resources.
		'''
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

		while current_device_points < target_device_points:
			if current_device_points >= max_device_points:
				break
			random_queries = randomwordgenerator.generate_random_words(num_searches)
			for query in random_queries:
				self.browser.type_and_submit(AttributeType.Name, 'q', query, clear_after_submit = True)
				self.browser.sleep(self.sleep_time)
			current_device_points = self.account_manager.get_daily_device_points()[0]

		self.account_manager.open_dashboard()
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
			self._perform_random_searches(num_searches)
			self.account_manager.sign_out()

def main():
	# Enter Hotmail/Outlook creds here.
	creds = []
	desktop_bot = BingRewardsBot(BrowserType.Chrome)
	desktop_bot.execute(creds, 30)
	desktop_bot.finish()

	#mobile_bot = BingRewardsBot(BrowserType.Chrome, is_mobile = True)
	#mobile_bot.execute(creds, 2)
	#mobile_bot.finish()

if __name__ == '__main__':
	main()