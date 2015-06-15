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
		self.browser = webdrivermanager.get_selenium_webdriver(browser_type, mobile)
		# Throw exception if browser is None.
		if url:
			self.browser.get(url)

	def _wait(self, attribute_type, attribute_value, wait_condition = ExpectedCondition.presence_of_element_located):
		attr = (attribute_type, attribute_value)
		try:
			WebDriverWait(self.browser, _WAIT_TIME_SECONDS).until(wait_condition(attr))
			wait_cond_satisfied = True
		except:
			wait_cond_satisfied = False
		return wait_cond_satisfied

	def _get_element(self, attribute_type, attribute_value, wait_condition = ExpectedCondition.presence_of_element_located):
		wait_successful = self._wait(attribute_type, attribute_value, wait_condition)
		count = 1
		while not wait_successful and count <= _NUM_RETRIES:
			self.sleep(_WAIT_TIME_SECONDS * count)
			wait_successful = self._wait(attribute_type, attribute_value, wait_condition)
			count = count + 1
		return self.browser.find_element(attribute_type, attribute_value) if wait_successful else None

	def open(self, url):
		self.browser.get(url)
		return self

	def click(self, attribute_type_enum, attribute_value):
		elem = self._get_element(attribute_type_enum.value, attribute_value, ExpectedCondition.element_to_be_clickable)
		if elem:
			elem.click()
		return self

	def clear(self, attribute_type_enum, attribute_value):
		elem = self._get_element(attribute_type_enum.value, attribute_value)
		if elem:
			elem.clear()
		return self

	def type(self, attribute_type_enum, attribute_value, message, press_enter = False):
		textfield = self._get_element(attribute_type_enum.value, attribute_value)
		if textfield:
			textfield.send_keys(message + Keys.RETURN if press_enter else message)
		return self

	def type_and_submit(self, textfields):
		target = None		
		for field_attr_type in textfields:
			field_attr_value_to_message = textfields[field_attr_type]
			for field_attr_value in field_attr_value_to_message:
				message = field_attr_value_to_message[field_attr_value]
				self.type(field_attr_type, field_attr_value, message)
		return self

	def sleep(self, num_seconds = _WAIT_TIME_SECONDS):
		WebDriverWait(self.browser, num_seconds)
		return self

	def close(self):
		self.browser.quit()
		self.browser = None