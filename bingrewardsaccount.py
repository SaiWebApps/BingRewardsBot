import enum

from browser_automation_utils.browser import AttributeType

# Constants
_SIGN_IN_URL = 'https://www.bing.com/rewards/signin'
_DASHBOARD_URL = 'https://www.bing.com/rewards/dashboard'
_MOBILE_SPECIAL_OFFERS_URL = 'https://www.bing.com/rewards/dashboard?showOffers=1'

DAILY_CURRENT_PC_OFFER_POINTS_XPATH = '//*[@id="credits"]/div[2]/span[1]/span'
DAILY_CURRENT_PC_POINTS_XPATH = '//div[@id="credits"]/div[2]/span[2]/span'
SPECIAL_OFFERS_PC_PARENT_XPATH = '//*[@id="dashboard_wrapper"]/div[1]/div[1]/ul'

DAILY_CURRENT_MOBILE_OFFER_POINTS_XPATH = '//*[@id="credit-progress"]/div[3]/span[1]'
DAILY_MAX_MOBILE_OFFER_POINTS_XPATH = '//*[@id="credit-progress"]/div[3]/span[2]'
DAILY_CURRENT_MOBILE_POINTS_XPATH = '//*[@id="credit-progress"]/div[5]/span[1]'
DAILY_MAX_MOBILE_POINTS_XPATH = '//*[@id="credit-progress"]/div[5]/span[2]'
SPECIAL_OFFERS_PARENT_XPATH = '//*[@id="activities"]/div[2]/div[1]'

# Decorators
def convert_result_to_uint(function):
    '''
        @description
            Convert the result(s) of the specified function to int(s).

        @param function
            Function whose output is being integer-ized (e.g., ['2','3']
            will be converted to [2,3])

        @return
            If function's output is a list, then convert each element
            to an int. Otherwise, just convert function output as is to int.
    '''
    def func_wrapper(*args, **kwargs):
        try:
            function_output = function(*args, **kwargs)
            # If the function result is a list, then de-stringify each
            # element in the list.
            if (type(function_output) == type([])):
                result = [int(elem) for elem in function_output]
            # Otherwise, it's just a single stringified number, so just
            # convert it back to to an int.
            else:
                result = int(function_output)
        except:
            result = int()
        return result
    return func_wrapper

def go_to_and_return_from(dest_url):
    '''
        @description
            Navigate to the specified url, execute the specified function,
            and then return to the original page.

        @param dest_url
            Url to navigate to before executing the function

        @param function
            Function to execute after navigating to dest_url

        @return
            The function's output as is
    '''
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

def open_stats_iframe(function):
    def func_wrapper(*args, **kwargs):
        args[0].browser.click(AttributeType.Id, 'id_rc')
        args[0].browser.switch_into_iframe(AttributeType.Id, 'bepfm')
        function_output = function(*args, **kwargs)
        args[0].browser.switch_out_of_iframe()
        return function_output
    return func_wrapper

# Classes
class AbstractAccountManager:
    def __init__(self, browser = None, account_creds = None):
        self.browser = browser
        self.account_creds = account_creds

    # Abstract Methods
    def get_device_class(self):
        raise NotImplementedError()

    def get_special_offer_links(self):
        raise NotImplementedError()

    def accumulate_special_offer_points(self):
        special_offers = self.get_special_offer_links()
        base_url = self.browser.get_current_url()
        for link in special_offers:
            self.browser.open(link)
        if self.browser.get_current_url() != base_url:
            self.browser.open(base_url)

    def get_total_num_points(self):
        raise NotImplementedError()

    def get_daily_device_points(self):
        raise NotImplementedError()

    def get_daily_offer_points(self):
        raise NotImplementedError()

    def _load_login_form(self):
        '''
            @description
                Perform some set of actions to move from the _SIGN_IN_URL to the
                actual sign in form.
        '''
        pass

    def open_dashboard(self):
        '''
            @description
                Navigate to the user's BingRewards dashboard page.
                Assumes that the user is already signed in.
        '''
        self.browser.open(_DASHBOARD_URL)

    def sign_in(self):
        '''
            @description
                Sign in to the specified Bing Rewards account.

            @return
                True if sign-in was successful, False otherwise
        '''
        self.browser.open(_SIGN_IN_URL)
        self._load_login_form()
        self.browser.type_and_submit_form(
            {
                AttributeType.Name: {
                    'loginfmt': self.account_creds.email,
                    'passwd': str(self.account_creds.password)
                }
            }
        )
        return (not self.browser.contains_element(AttributeType.Id, 'idTd_Tile_ErrorMsg_Login'))

    def sign_out(self):
        pass

    def __str__(self):
        '''
            abc@def.com - 2200 points
            Daily Point Breakdown:
                Daily [PC/Mobile/DeviceClass] Points = 15/15
                Daily Offer Points = 5/5
        '''
        account_details = [self.account_creds.email, ' - ', str(self.get_total_num_points()), \
            ' points\n']
        account_details.append('Daily Point Breakdown:\n')

        daily_device_points =   '/'.join([str(elem) for elem in self.get_daily_device_points()])
        account_details.extend(['\tDaily ', self.get_device_class(), ' Points = ', \
            daily_device_points, '\n'])

        daily_offer_points = '/'.join([str(elem) for elem in self.get_daily_offer_points()])
        account_details.extend(['\tDaily Offer Points = ', daily_offer_points, '\n'])
        
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

    @convert_result_to_uint
    @open_stats_iframe
    def _get_daily_statistics(self, target_xpath):
        '''
            @description
                Navigate to the Bing Rewards dashboard, open the points flyout,
                and get the specified daily statistic.

            @param target_xpath
                XPath of the target daily stat element

            @return
                A 2-element list, where the first element is the current get_value
                of the daily stat, and the second is the max possible value for that 
                stat. If we are unable to read either value, then return [-1,-1].
        '''
        output = [-1, -1]
        daily_points = self.browser.get_value(AttributeType.XPath, target_xpath)
        if daily_points:
            output = daily_points.split('/')
        return output

    def get_device_class(self):
        return 'PC'

    @go_to_and_return_from(_DASHBOARD_URL)
    def get_special_offer_links(self):
        return self.browser.get_child_attributes(AttributeType.XPath, \
            SPECIAL_OFFERS_PC_PARENT_XPATH, 'href', 2)

    @convert_result_to_uint
    def get_total_num_points(self):
        return self.browser.get_value(AttributeType.Id, 'id_rc')

    def get_daily_device_points(self):
        return self._get_daily_statistics(DAILY_CURRENT_PC_POINTS_XPATH)

    def get_daily_offer_points(self):
        return self._get_daily_statistics(DAILY_CURRENT_PC_OFFER_POINTS_XPATH)

    def sign_out(self):
        self.browser.click(AttributeType.Id, 'id_n')
        self.browser.sleep(5)
        self.browser.click(AttributeType.XPath, '//*[@id="b_idProviders"]/li/a/span[2]')
        self.browser.sleep(5)
        return self.browser.get_value(AttributeType.Id, 'id_n') and \
            self.browser.get_value(AttributeType.Id, 'id_n').strip() != ''

class MobileAccountManager(AbstractAccountManager):
    def get_device_class(self):
        return 'Mobile'

    @go_to_and_return_from(_MOBILE_SPECIAL_OFFERS_URL)
    def get_special_offer_links(self):
        return self.browser.get_child_attributes(AttributeType.XPath, SPECIAL_OFFERS_PARENT_XPATH, 'href')[:-3]

    @convert_result_to_uint
    @go_to_and_return_from(_DASHBOARD_URL)
    def get_total_num_points(self):
        return self.browser.get_value(AttributeType.XPath, '//*[@id="status-bar"]/span')
    
    @convert_result_to_uint
    @go_to_and_return_from(_DASHBOARD_URL)
    def get_daily_device_points(self):
        current_mobile_points = self.browser.get_value(AttributeType.XPath, DAILY_CURRENT_MOBILE_POINTS_XPATH)
        maximum_mobile_points = self.browser.get_value(AttributeType.XPath, DAILY_MAX_MOBILE_POINTS_XPATH).strip('/')
        return [current_mobile_points if current_mobile_points else -1, \
            maximum_mobile_points if maximum_mobile_points else -1]

    @convert_result_to_uint
    @go_to_and_return_from(_DASHBOARD_URL)
    def get_daily_offer_points(self):
        current_offer_points = self.browser.get_value(AttributeType.XPath, DAILY_CURRENT_MOBILE_OFFER_POINTS_XPATH)
        maximum_offer_points = self.browser.get_value(AttributeType.XPath, DAILY_MAX_MOBILE_OFFER_POINTS_XPATH).strip('/')
        return [current_offer_points if current_offer_points else -1, \
            maximum_offer_points if maximum_offer_points else -1]