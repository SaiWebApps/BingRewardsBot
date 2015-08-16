import enum
from browser.browser import AttributeType

# Constants
_SIGN_IN_URL = 'https://www.bing.com/rewards/signin'
_DASHBOARD_URL = 'https://www.bing.com/rewards/dashboard'
_PROFILE_URL = 'https://www.bing.com/rewards/settings/profileframed'

DAILY_PC_OFFER_POINTS_XPATH = '//*[@id="credits"]/div[2]/span[1]/span'
DAILY_PC_POINTS_XPATH = '//div[@id="credits"]/div[2]/span[2]/span'
DAILY_MOBILE_OFFER_POINTS_XPATH = '//*[@id="credit-progress"]/div[3]/span[1]'
DAILY_MOBILE_OFFER_MAX_POINTS_XPATH = '//*[@id="credit-progress"]/div[3]/span[2]'
DAILY_CURRENT_MOBILE_POINTS_XPATH = '//*[@id="credit-progress"]/div[5]/span[1]'
DAILY_MAX_MOBILE_POINTS_XPATH = '//*[@id="credit-progress"]/div[5]/span[2]'

# Decorators
def convert_result_to_uint(function):
	def func_wrapper(*args, **kwargs):
		try:
			function_output = function(*args, **kwargs)
			if (type(function_output) == type([])):
				result = [int(elem) for elem in function_output]
			else:
				result = int(function_output)
		except:
			result = int()
		return result
	return func_wrapper

def go_to_and_return_from(dest_url):
	def page_nav_decorator(function):
		def func_wrapper(*args, **kwargs):
			browser = args[0].browser
			orig_url = browser.get_current_url()
			# Go to destination.
			if orig_url != dest_url:
				browser.open(dest_url)
			# Execute function.
			function_output = function(*args, **kwargs)
			# Come back to source.
			if orig_url != dest_url:
				browser.open(orig_url)
			return function_output
		return func_wrapper
	return page_nav_decorator

class AccountCredentials:
	def __init__(self, email, password):
		self.email = email
		self.password = password

class AbstractAccountManager:
	def __init__(self, browser, account_creds = None):
		self.browser = browser
		self.account_creds = account_creds

	# Abstract Methods
	def get_total_num_points(self):
		raise NotImplementedError()

	def get_daily_device_points(self):
	    raise NotImplementedError()

	def get_daily_offer_points(self):
		raise NotImplementedError()

	def sign_out(self):
		raise NotImplementedError()

	# Login-related methods
	def _load_login_form(self):
		'''
			Perform some set of actions to move from the _SIGN_IN_URL to the
			actual sign in form.
		'''
		pass

	def open_dashboard(self):
		self.browser.open(_DASHBOARD_URL)

	def sign_in(self):
		'''
			@return
				True if sign-in was successful, False otherwise
		'''
		self.browser.open(_SIGN_IN_URL)
		self._load_login_form()
		self.browser.type_and_submit_form(
			{
				AttributeType.Name: {
					'loginfmt': self.account_creds.email,
					'passwd': self.account_creds.password
				}
			}
		)
		return (not self.browser.contains_element(AttributeType.Id, 'idTd_Tile_ErrorMsg_Login'))


	def __str__(self):
		'''
			abc@def.com - 2200 points
			Daily Point Breakdown:
				Daily Offer Points = 5
		'''
		account_details = [self.account_creds.email, ' - ', str(self.get_total_num_points()), ' points\n']
		account_details.append('Daily Point Breakdown:\n')
		daily_offer_points = [str(elem) for elem in self.get_daily_offer_points()]
		account_details.extend(['\tDaily Offer Points = ', daily_offer_points[0], '/', daily_offer_points[1], '\n'])
		return ''.join(account_details)

class DesktopAccountManager(AbstractAccountManager):
	def _load_login_form(self):
		'''
			The _SIGN_IN_URL on desktop does not immediately display the login form.
			Instead, the user must press a "Sign-In" button, which then redirects her
			to the actual login form.
		'''
		if self.browser.contains_element(AttributeType.Name, 'loginfmt'):
			return
		self.browser.click(AttributeType.Id, 'id_s')
		self.browser.click(AttributeType.ClassName, 'id_link_text')

	def sign_out(self):
		self.browser.click(AttributeType.Id, 'id_l')
		self.browser.sleep(5)
		self.browser.click(AttributeType.XPath, '//*[@id="b_idProviders"]/li/a')
		self.browser.sleep(5)
		return self.browser.get_value(AttributeType.Id, 'id_n').strip() != ''

	@convert_result_to_uint
	@go_to_and_return_from(_DASHBOARD_URL)
	def get_total_num_points(self):
		return self.browser.get_value(AttributeType.Id, 'id_rc')

	@convert_result_to_uint
	@go_to_and_return_from(_DASHBOARD_URL)
	def get_daily_device_points(self):
		self.browser.click(AttributeType.Id, 'id_rh')
		self.browser.switch_into_iframe(AttributeType.Id, 'bepfm')
		daily_pc_points = self.browser.get_value(AttributeType.XPath, DAILY_PC_POINTS_XPATH)
		self.browser.switch_out_of_iframe()
		return daily_pc_points.split('/')

	@convert_result_to_uint
	@go_to_and_return_from(_DASHBOARD_URL)
	def get_daily_offer_points(self):
		self.browser.click(AttributeType.Id, 'id_rh')
		self.browser.switch_into_iframe(AttributeType.Id, 'bepfm')
		daily_offer_points = self.browser.get_value(AttributeType.XPath, DAILY_PC_OFFER_POINTS_XPATH)
		self.browser.switch_out_of_iframe()
		return daily_offer_points.split('/')

	def __str__(self):
		'''
			abc@def.com - 2200 points
			Daily Point Breakdown:
				Daily Offer Points = 5
				Daily PC Points = 15
		'''
		account_details = super().__str__()
		daily_device_points = [str(elem) for elem in self.get_daily_device_points()]
		account_details += '\tDaily PC Points = ' + daily_device_points[0] + '/' + daily_device_points[1] + '\n'
		return account_details

class MobileAccountManager(AbstractAccountManager):
	def sign_out(self):
		self.browser.open(_PROFILE_URL)
		return self.browser.click(AttributeType.XPath, '//*[@id="pf"]/div[2]/a[2]')

	@convert_result_to_uint
	@go_to_and_return_from(_DASHBOARD_URL)
	def get_total_num_points(self):
		return self.browser.get_value(AttributeType.XPath, '//*[@id="status-bar"]/span')
	
	@convert_result_to_uint
	@go_to_and_return_from(_DASHBOARD_URL)
	def get_daily_device_points(self):
		return [self.browser.get_value(AttributeType.XPath, DAILY_CURRENT_MOBILE_POINTS_XPATH), \
			self.browser.get_value(AttributeType.XPath, DAILY_MAX_MOBILE_POINTS_XPATH)]

	@convert_result_to_uint
	@go_to_and_return_from(_DASHBOARD_URL)
	def get_daily_offer_points(self):
		return [self.browser.get_value(AttributeType.XPath, DAILY_MOBILE_OFFER_POINTS_XPATH), \
			self.browser.get_value(AttributeType.XPath, DAILY_MOBILE_OFFER_MAX_POINTS_XPATH)]

	def __str__(self):
		'''
			abc@def.com - 2200 points
			Daily Point Breakdown:
				Daily Offer Points = 5
				Daily Mobile Points = 10
		'''
		account_details = super().__str__()
		daily_device_points = [str(elem) for elem in self.get_daily_device_points()]
		account_details += '\tDaily Mobile Points = ' + daily_device_points[0] + '/' + daily_device_points[1] + '\n'
		return account_details