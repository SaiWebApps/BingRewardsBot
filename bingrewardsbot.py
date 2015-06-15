import sys

from browser.browser import Browser, AttributeType
from browser.webdrivermanager.browsertypes import BrowserType
from randomwordgenerator import randomwordgenerator

class AccumulatePointsStrategy:
	def __init__(self, browser_type, is_mobile, url):
		self.browser = Browser(browser_type, mobile = is_mobile, url = url)

	def sign_in(self, email, password):
		login_form = {
			AttributeType.Name: {
				'login': email,
				'passwd': password
			}
		}
		return login_form

	def perform_random_searches(self, num_searches = 1):
		random_queries = randomwordgenerator.generate_random_words(num_searches)
		for query in random_queries:
			self.browser.type(AttributeType.Name, 'q', query, press_enter = True)

	def finish(self):
		self.browser.close()

	def execute(self, email, password, num_searches):
		self.sign_in(email, password)
		self.perform_random_searches(num_searches)
		self.finish()

class BingDesktopStrategy(AccumulatePointsStrategy):
	def __init__(self, browser_type):
		super().__init__(browser_type = browser_type, is_mobile = False, \
			url = 'http://www.bing.com')

	def sign_in(self, email, password):
		login_form = super().sign_in(email, password)
		self.browser.click(AttributeType.Id, 'id_s') \
			.click(AttributeType.ClassName, 'id_link_text') \
			.type_and_submit(login_form)

class BingMobileStrategy(AccumulatePointsStrategy):
	def __init__(self, browser_type):
		super().__init__(browser_type = browser_type, is_mobile = True, \
			url = 'http://www.bing.com/rewards/signin')

	def sign_in(self, email, password):
		login_form = super().sign_in(email, password)
		self.browser.type_and_submit(login_form).open('http://www.bing.com')

def main():
	creds = []	# Enter Hotmail/Outlook creds here.
	for user in creds:
		strategy = BingDesktopStrategy(BrowserType.Chrome)
		strategy.execute(user['email'], user['password'], 30)

	for user in creds:
		strategy = BingMobileStrategy(BrowserType.Chrome)
		strategy.execute(user['email'], user['password'], 20)

if __name__ == '__main__':
	main()