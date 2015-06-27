from browser.browser import Browser, AttributeType
from randomwordgenerator import randomwordgenerator

# Abstract class for accumulating Bing Rewards points
class AccumulatePointsStrategy:
	def __init__(self, browser_type, is_mobile, url):
		'''
			@param browser_type
				BrowserType enum value specifying the type of browser that
				the user wants to utilize for search automation + points accumulation

			@param is_mobile
				Boolean indicating whether the strategy is for accumulating
				mobile-based (if True) or desktop-based (if False) rewards points.

			@param url
				URL that the browser will opened with.
		'''
		self.browser = Browser(browser_type, mobile = is_mobile, url = url)

	def sign_in(self, email, password):
		'''
			@param email
				Hotmail/Outlook email address of user trying to accumulate points

			@param password
				Password of said user

			@return
				a dictionary containing the fields in the Bing Rewards Account Login form
		'''
		login_form = {
			AttributeType.Name: {
				'login': email,
				'passwd': password
			}
		}
		return login_form

	def perform_random_searches(self, num_searches = 1):
		'''
			@param num_searches
				(Optional - 1 by default) Number of Bing searches that the
				user wants to automate.
		'''
		# Use randomwordgenerator API to generate num_searches random words.
		# Then, pass them over to Bing as search queries.
		random_queries = randomwordgenerator.generate_random_words(num_searches)
		for query in random_queries:
			self.browser.type_and_submit(AttributeType.Name, 'q', query, clear_after_submit = True)

	def finish(self):
		'''
			Close the browser, and release all resources.
		'''
		self.browser.close()
		self.browser = None

	def execute(self, email, password, num_searches):
		'''
			@param email, password
				(Required) User's Hotmail/Outlook email address & password; 
				needed to accumulate points under this user's account

			@param num_searches
				(Required) Number of Bing searches that user with given
				credentials wants to automate.
		'''
		self.sign_in(email, password)
		self.perform_random_searches(num_searches)
		self.finish()

# Bing searches on desktop browser
class BingDesktopStrategy(AccumulatePointsStrategy):
	def __init__(self, browser_type):
		super().__init__(browser_type = browser_type, is_mobile = False, \
			url = 'http://www.bing.com')

	def sign_in(self, email, password):
		login_form = super().sign_in(email, password)
		self.browser.click(AttributeType.Id, 'id_s') \
			.click(AttributeType.ClassName, 'id_link_text') \
			.type_and_submit_form(login_form)

# Bing searches on mobile browser
class BingMobileStrategy(AccumulatePointsStrategy):
	def __init__(self, browser_type):
		super().__init__(browser_type = browser_type, is_mobile = True, \
			url = 'http://www.bing.com/rewards/signin')

	def sign_in(self, email, password):
		login_form = super().sign_in(email, password)
		self.browser.type_and_submit_form(login_form).open('http://www.bing.com')