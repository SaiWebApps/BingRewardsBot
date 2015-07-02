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
		self.is_mobile = is_mobile

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

	def get_num_rewards_points(self, login_creds = None):
		'''
			@param login_creds
				(Optional) Tuple where 1st element = email, 2nd = password for a Bing Rewards account;
				if not specified, then assume that the user has already signed in.

			@return
				The total number of Bing Rewards points accumulated by some user.
		'''
		# If login creds are specified, then the user has not signed in yet, so sign in to the
		# specified account.
		if login_creds:
			self.sign_in(login_creds[0], login_creds[1])
		# Give some time for sign-in to sink in - it takes some time for the # of points to be updated.
		self.browser.sleep(10)
		return 0	# Let children determine the impl specifics.

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
		print('Automating searches for ', email, '(Mobile = ', str(self.is_mobile), '): ')
		self.sign_in(email, password)

		print('\tInitial # of Points = ' + str(self.get_num_rewards_points()))
		self.perform_random_searches(num_searches)
		print('\tFinal # of Points = ' + str(self.get_num_rewards_points()) + '\n')

		self.finish()

# Bing searches on desktop browser
class BingDesktopStrategy(AccumulatePointsStrategy):
	def __init__(self, browser_type):
		super().__init__(browser_type = browser_type, is_mobile = False, \
			url = 'http://www.bing.com')

	def get_num_rewards_points(self, login_creds = None):
		super().get_num_rewards_points(login_creds)	# Login if necessary.
		num_points = self.browser.get_value(AttributeType.Id, 'id_rc')
		return num_points if num_points else 0

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

	def get_num_rewards_points(self, login_creds = None):
		super().get_num_rewards_points(login_creds)
		dashboard_url = 'https://www.bing.com/rewards/dashboard'
		if self.browser.get_current_url() != dashboard_url:
			self.browser.open(dashboard_url)
		num_points = self.browser.get_value(AttributeType.XPath, '//div[@id="status-bar"]/span')
		self.browser.open('http://www.bing.com')
		return num_points if num_points else 0

	def sign_in(self, email, password):
		login_form = super().sign_in(email, password)
		self.browser.type_and_submit_form(login_form)