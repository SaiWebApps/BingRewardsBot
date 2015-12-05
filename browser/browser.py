import enum
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedCondition

from webdrivermanager import webdrivermanager

_WAIT_TIME_SECONDS = 10
_NUM_RETRIES = 2

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
        if url:
            self.browser.get(url)

    def _wait(self, attribute_type, attribute_value, wait_condition = \
            ExpectedCondition.presence_of_element_located):
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

    def __try_finding_element(self, attribute_type_enum, attribute_value, wait_condition = \
            ExpectedCondition.presence_of_element_located, num_retries = _NUM_RETRIES):
        '''
            @params attribute_type, attribute_value, wait_condition
                (1st 2 required, 3rd optional) See descriptions in _wait above.

            @params num_retries
                (Optional) # of times script needs to back off and wait for element
                to be loaded if it can't be found yet

            @return
                True if wait condition was ever satisfied and specified element(s)
                were found, False otherwise.
        '''
        attribute_type = attribute_type_enum.value

        # Try to get the element num_retries times (best effort). After that, if
        # the element still can't be retrieved, return None.
        wait_successful = self._wait(attribute_type, attribute_value, wait_condition)
        count = 1
        while not wait_successful and count <= num_retries:
            self.sleep(_WAIT_TIME_SECONDS)
            wait_successful = self._wait(attribute_type, attribute_value, wait_condition)
            print('Retry #' + str(count) + '/' + str(num_retries)  + ' for ' + attribute_value)
            count = count + 1
            self.browser.get(self.browser.current_url)  # Refresh the page.

        return wait_successful

    def _get_element(self, attribute_type_enum, attribute_value, wait_condition = \
            ExpectedCondition.presence_of_element_located, num_retries = _NUM_RETRIES):
        '''
            @params attribute_type, attribute_value, wait_condition
                (1st 2 required, 3rd optional) See descriptions in _wait above.

            @params num_retries
                (Optional) # of times script needs to back off and wait for element
                to be loaded if it can't be found yet

            @return
                - The Selenium WebElement with the specified attributes (e.g., if
                attribute_type = AttributeType.Name and attribute_value = login,
                then return the element with name="login").
                - None if there is no such element.
        '''
        target_element = None
        if self.__try_finding_element(attribute_type_enum, attribute_value, wait_condition, num_retries):
            target_element = self.browser.find_element(attribute_type_enum.value, attribute_value)
        return target_element

    def _get_elements(self, attribute_type_enum, attribute_value, wait_condition = \
            ExpectedCondition.presence_of_element_located, num_retries = _NUM_RETRIES):
        '''
            @params attribute_type, attribute_value, wait_condition
                (1st 2 required, 3rd optional) See descriptions in _wait above.

            @params num_retries
                (Optional) # of times script needs to back off and wait for element
                to be loaded if it can't be found yet

            @return
                - The list of Selenium WebElements with the specified attributes (e.g., if
                  attribute_type = AttributeType.Name and attribute_value = login, then
                  return the element with name="login").
                - Empty list if there is no such element.
        '''
        target_elements = []
        if self.__try_finding_element(attribute_type_enum, attribute_value, wait_condition, num_retries):
            target_elements = self.browser.find_elements(attribute_type_enum.value, attribute_value)
        return target_elements

    def _get_child_elements(self, parent_attribute_type_enum, parent_attribute_value, num_levels):
        parent_element = self._get_element(parent_attribute_type_enum, parent_attribute_value)
        children_xpath = '.' + ('//*' * num_levels)
        return parent_element.find_elements(AttributeType.XPath.value, children_xpath) if parent_element else []

    def open(self, url):
        '''
            @param url
                (Required) URL to open within this browser.

            @return
                True if the browser's url has been successfully set to url,
                False otherwise.
        '''
        self.browser.get(url)
        self.sleep(_WAIT_TIME_SECONDS)
        return self.browser.current_url == url

    def click(self, attribute_type_enum, attribute_value):
        ''' 
            @param attribute_type_enum
                An AttributeType enum value (e.g., AttributeType.Name).

            @param attribute_value
                The value corresponding to attribute_type_enum (as in login 
                in <input name="login">).

            @return
                True if the specified element was found and clicked successfully,
                False otherwise.
        '''
        elem = self._get_element(attribute_type_enum, attribute_value, ExpectedCondition.element_to_be_clickable)
        if not elem:
            return False
        elem.click()
        return True

    def clear(self, attribute_type_enum, attribute_value):
        '''
            Clear the specified element (presumed to be a textfield).
            
            @param attribute_type_enum, attribute_value
                (Required) <input name="login" /> -> AttributeType.Name, "login"

            @return
                True if element was found and cleared successfully, False otherwise.
        '''
        elem = self._get_element(attribute_type_enum, attribute_value)
        if not elem:
            return False
        elem.clear()
        return True

    def type(self, attribute_type_enum, attribute_value, message):
        '''
            Type message into the specified textfield.
            
            @param attribute_type_enum, attribute_value
                (Required) <input name="login" /> -> AttributeType.Name, "login"

            @param message
                (Required) Message to type in the target element.

            @return
                True if textfield was found and message was typed into textfield,
                False otherwise.
        '''
        textfield = self._get_element(attribute_type_enum, attribute_value)
        if not textfield:
            return False
        textfield.send_keys(message)
        return True

    def submit(self, attribute_type_enum, attribute_value):
        '''
            Call on a form field to submit the entire form.

            @param attribute_type_enum, attribute_value
                (Required) <input type="submit" id="Submit" /> -> AttributeType.ID, "Submit"

            @return
                True if the field was found and was submitted successfully, False otherwise.
        '''
        field = self._get_element(attribute_type_enum, attribute_value)
        if not field:
            return False
        field.submit()
        return True

    def type_and_submit(self, attribute_type_enum, attribute_value, message, clear_after_submit = False):
        '''
            @param attribute_type_enum, attribute_value
                (Required) <input name="login" /> -> AttributeType.Name, "login"

            @param message
                (Required) Message to type into specified textfield.

            @param clear_after_submit
                (Optional) Boolean indicating whether textfield should be cleared after form submission.

            @return
                True if the textfield was found, message was typed into it, the form as a
                whole was submitted successfully, and the textfield was cleared afterwards.
                False otherwise.
        '''
        status = self.type(attribute_type_enum, attribute_value, message) and \
            self.submit(attribute_type_enum, attribute_value)
        if clear_after_submit:
            status = status and self.clear(attribute_type_enum, attribute_value)
        return status

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
        status = True

        field_attr_type_enum = None
        field_attr_value = None

        for field_attr_type_enum in textfields:
            field_attr_values = textfields[field_attr_type_enum]
            for field_attr_value in field_attr_values:
                # Find each field, and type the specified message into it.
                message = field_attr_values[field_attr_value]
                status = status and self.type(field_attr_type_enum, field_attr_value, message)
                self.sleep(1)

        if field_attr_type_enum and field_attr_value:
            status = status and self.submit(field_attr_type_enum, field_attr_value)
        
        return status

    def contains_element(self, attribute_type_enum, attribute_value):
        '''
            For <span id="example"> Value </span>:
                @param attribute_type_enum = AttributeType.id
                @param attribute_value = "example"
                @return True if found, False otherwise
        '''
        return self._get_element(attribute_type_enum, attribute_value, num_retries = 0) is not None

    def get_value(self, attribute_type_enum, attribute_value):
        '''
            For <span id="example"> Value </span>:
                @param attribute_type_enum = AttributeType.id
                @param attribute_value = "example"
                @return "Value"

            But if there is no element with id = "example", then return None.
        '''
        target_elem = self._get_element(attribute_type_enum, attribute_value)
        return target_elem.text if target_elem else None

    def get_all_values(self, attribute_type_enum, attribute_value):
        '''
            Similar to get_value, but now suppose that we are dealing with:
                <span class="example"> Value </span>
            There could be multiple span elements with class ".example," and
            this method returns the values for all such span elements.

            For the above span, attribute_type_enum = AttributeType.ClassName
            and attribute_value = "example".
        '''
        target_elements = self._get_elements(attribute_type_enum, attribute_value)
        return [elem.text.encode('ascii', 'ignore') for elem in target_elements]

    def get_target_attribute(self, attribute_type_enum, attribute_value, target_attribute):
        target_elem = self._get_element(attribute_type_enum, attribute_value)
        return target_elem.get_attribute(target_attribute) if target_elem else None

    def get_all_target_attributes(self, attribute_type_enum, attribute_value, target_attribute):
        target_elements = self._get_elements(attribute_type_enum, attribute_value)
        return [elem.get_attribute(target_attribute) for elem in target_elements]

    def get_child_values(self, parent_attribute_type_enum, parent_attribute_value, num_levels = 1):
        return [element.text.encode('ascii', 'ignore') for element in self._get_child_elements(parent_attribute_type_enum, parent_attribute_value, num_levels)]

    def get_child_attributes(self, parent_attribute_type_enum, parent_attribute_value, target_attribute, num_levels = 1):
        child_elements = self._get_child_elements(parent_attribute_type_enum, parent_attribute_value, num_levels)
        child_attributes = [element.get_attribute(target_attribute) for element in child_elements]
        return [elem for elem in child_attributes if elem]

    def get_current_url(self):
        '''
            @return 
                the url of the page that the browser is currently displaying
        '''
        return self.browser.current_url

    def sleep(self, num_seconds = _WAIT_TIME_SECONDS):
        '''
            @param num_seconds
                Number of seconds that browser should pause/wait before moving
                on to an automated task.
        '''
        time.sleep(num_seconds)

    def switch_into_iframe(self, attribute_type_enum, attribute_value):
        '''
            @param attribute_type_enum, attribute_value
                Attributes of target IFrame.
                <iframe id="random">....</iframe>
                attribute_type_enum = AttributeType.Id
                attribute_value = "random"

            @return
                True if the iframe was found and browser shifted focus onto it.
                False otherwise.
        '''
        target_iframe = self._get_element(attribute_type_enum, attribute_value)
        if not target_iframe:
            return False
        self.browser.switch_to.frame(target_iframe)
        return True

    def switch_out_of_iframe(self):
        '''
            Shift focus back onto parent frame (IFrame container).
        '''
        self.browser.switch_to.default_content()

    def close(self):
        '''
            @description
                Close this browser window.
        '''
        if self.browser:
            self.browser.quit()
        self.browser = None