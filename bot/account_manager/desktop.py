import enum

from browser_automation_utils.browser import AttributeType
from base import *
from decorators import *

# Constants
DAILY_CURRENT_PC_OFFER_POINTS_XPATH = '//*[@id="credits"]/div[2]/span[1]/span'
DAILY_CURRENT_PC_POINTS_XPATH = '//div[@id="credits"]/div[2]/span[2]/span'
SPECIAL_OFFERS_PC_PARENT_XPATH = '//*[@id="dashboard_wrapper"]/div[1]/div[1]/ul'

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

    @go_to_and_return_from(DASHBOARD_URL)
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