import enum

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedCondition

from webdrivermanager import webdrivermanager

_WAIT_TIME_SECONDS = 30
_NUM_RETRIES = 10

class AttributeType(enum.Enum):
	Id = By.ID
	ClassName = By.CLASS_NAME
	Name = By.NAME
	XPath = By.XPATH
	CssSelector = By.CSS_SELECTOR
	TagName = By.TAG_NAME
	LinkText = By.LINK_TEXT

class Browser:
	def __init__(self, browser_type, url = None, mobile = False):
		'''
			@param browser_type
				(Required) A webdrivermanager.browsertypes.BrowserType enum value
				that specifies the type of browser to use for automation.

			@param url
				(Optional) Website under automation

			@param mobile
				(Optional) If true, emulate a mobile browser; otherwise, operate
				like a desktop browser (the default behavior).
		'''
		self.browser = webdrivermanager.get_selenium_webdriver(browser_type, mobile)
		# Throw exception if browser is None.
		if url:
			self.browser.get(url)

	def _wait(self, attribute_type, attribute_value, wait_condition = ExpectedCondition.presence_of_element_located):
		'''
			@param attribute_type
				(Required) AttributeType enum value; specifies which type of attribute
				the browser should wait for.

			@param attribute_value
				(Required) The value corresponding to the AttributeType (e.g., given
				attribute_type=AttributeType.Name, this could be "login," which would
				mean that we are waiting for a field where name="login")

			@param wait_condition
				(Optional) Specify what event we should be waiting for with respect to
				the specified field; by default, we just wait until we can locate the
				element on the web page.

			@return
				True if the wait_condition was satisified (e.g., we find the element),
				False if not.
		'''
		attr = (attribute_type, attribute_value)
		try:
			WebDriverWait(self.browser, _WAIT_TIME_SECONDS).until(wait_condition(attr))
			wait_cond_satisfied = True
		except:
			wait_cond_satisfied = False
		return wait_cond_satisfied

	def _get_element(self, attribute_type, attribute_value, wait_condition = \
			ExpectedCondition.presence_of_element_located):
		'''
			@params attribute_type, attribute_value, wait_condition
				(Required) See descriptions in _wait above.

			@return
				- The Selenium WebElement with the specified attributes (e.g., if
				attribute_type = AttributeType.Name and attribute_value = login,
				then return the element with name="login").
				- None if there is no such element.
		'''
		# Try to get the element _NUM_RETRIES times (best effort). After that, if
		# the element still can't be retrieved, return None.
		wait_successful = self._wait(attribute_type, attribute_value, wait_condition)
		count = 1
		while not wait_successful and count <= _NUM_RETRIES:
			self.sleep(_WAIT_TIME_SECONDS * count)
			wait_successful = self._wait(attribute_type, attribute_value, wait_condition)
			print('Retry #' + str(count) + '/' + str(_NUM_RETRIES)  + 'for ' + attribute_value)
			count = count + 1
		return self.browser.find_element(attribute_type, attribute_value) if wait_successful else None

	def open(self, url):
		'''
			@param url
				(Required) URL to open within this browser.

			@return
				This Browser object, so that we can perform chained calls.
		'''
		self.browser.get(url)
		return self

	def click(self, attribute_type_enum, attribute_value):
		''' 
			@param attribute_type_enum
				An AttributeType enum value (e.g., AttributeType.Name).

			@param attribute_value
				The value corresponding to attribute_type_enum (as in login 
				in <input name="login">).

			@return
				This Browser object, so that we can perform chained calls.
		'''
		elem = self._get_element(attribute_type_enum.value, attribute_value, ExpectedCondition.element_to_be_clickable)
		if elem:
			elem.click()
		return self

	def clear(self, attribute_type_enum, attribute_value):
		'''
			Clear the specified element (presumed to be a textfield).
			
			@param attribute_type_enum, attribute_value
				(Required) <input name="login" /> -> AttributeType.Name, "login"
		'''
		elem = self._get_element(attribute_type_enum.value, attribute_value)
		if elem:
			elem.clear()
		return self

	def type(self, attribute_type_enum, attribute_value, message):
		'''
			Type message into the specified textfield.
			
			@param attribute_type_enum, attribute_value
				(Required) <input name="login" /> -> AttributeType.Name, "login"

			@param message
				(Required) Message to type in the target element.

			@return
				This Browser object, so that we can perform chained calls.
		'''
		textfield = self._get_element(attribute_type_enum.value, attribute_value)
		if textfield:
			textfield.send_keys(message)
		return self

	def submit(self, attribute_type_enum, attribute_value):
		'''
			Call on a form field to submit the entire form.

			@param attribute_type_enum, attribute_value
				(Required) <input type="submit" id="Submit" /> -> AttributeType.ID, "Submit"

			@return
				This Browser object, so that we can perform chained calls.
		'''
		field = self._get_element(attribute_type_enum.value, attribute_value)
		if field:
			field.submit()
		return self

	def type_and_submit(self, attribute_type_enum, attribute_value, message, clear_after_submit = False):
		'''
			@param attribute_type_enum, attribute_value
				(Required) <input name="login" /> -> AttributeType.Name, "login"

			@param message
				(Required) Message to type into specified textfield.

			@param clear_after_submit
				(Optional) Boolean indicating whether textfield should be cleared after form submission.

			@return
				This Browser object, so that we can perform chained calls.
		'''
		self.type(attribute_type_enum, attribute_value, message)
		self.submit(attribute_type_enum, attribute_value)
		if clear_after_submit:
			self.clear(attribute_type_enum, attribute_value)
		return self

	def type_and_submit_form(self, textfields):
		'''
			@param textfields
				Given this form:
					<form>
						<input type="text" name="login" /> : User types "email address."
						<input type="text" name="password" /> : User types "password."
						<input type="text" id="first_name" /> : User types "first name."
					</form>

			 	textfields shall equal the following:
				{
					AttributeType.Name: {
						'login': 'email address',
						'password': 'password'
					},
					AttributeType.Id: {
						'first_name': 'first name'
					}
				}

			@return
				This Browser object, so that we can perform chained calls.
		'''
		field_attr_type_enum = None
		field_attr_value = None

		for field_attr_type_enum in textfields:
			field_attr_values = textfields[field_attr_type_enum]
			for field_attr_value in field_attr_values:
				message = field_attr_values[field_attr_value]
				self.type(field_attr_type_enum, field_attr_value, message)

		if field_attr_type_enum and field_attr_value:
			self.submit(field_attr_type_enum, field_attr_value)
		
		return self

	def sleep(self, num_seconds = _WAIT_TIME_SECONDS):
		'''
			@param num_seconds
				Number of seconds that browser should pause/wait
				before moving on to an automated task.

			@return
				This Browser object (enables calls to be chained).
		'''
		WebDriverWait(self.browser, num_seconds)
		return self

	def close(self):
		'''
			Close this browser window.
		'''
		self.browser.quit()
		self.browser = None	# So that we don't use this by accident.