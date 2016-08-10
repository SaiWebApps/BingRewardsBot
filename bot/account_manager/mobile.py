from browser_automation_utils.browser import AttributeType
from base import *
from decorators import *

# Constants
_MOBILE_SPECIAL_OFFERS_URL = 'https://www.bing.com/rewards/dashboard?showOffers=1'
DAILY_CURRENT_MOBILE_OFFER_POINTS_XPATH = '//*[@id="credit-progress"]/div[3]/span[1]'
DAILY_MAX_MOBILE_OFFER_POINTS_XPATH = '//*[@id="credit-progress"]/div[3]/span[2]'
DAILY_CURRENT_MOBILE_POINTS_XPATH = '//*[@id="credit-progress"]/div[5]/span[1]'
DAILY_MAX_MOBILE_POINTS_XPATH = '//*[@id="credit-progress"]/div[5]/span[2]'
SPECIAL_OFFERS_PARENT_XPATH = '//*[@id="activities"]/div[2]/div[1]'

class MobileAccountManager(AbstractAccountManager):
    def get_device_class(self):
        return 'Mobile'

    @go_to_and_return_from(_MOBILE_SPECIAL_OFFERS_URL)
    def get_special_offer_links(self):
        return self.browser.get_child_attributes(AttributeType.XPath, SPECIAL_OFFERS_PARENT_XPATH, 'href')[:-3]

    @convert_result_to_uint
    @go_to_and_return_from(DASHBOARD_URL)
    def get_total_num_points(self):
        return self.browser.get_value(AttributeType.XPath, '//*[@id="status-bar"]/span')
    
    @convert_result_to_uint
    @go_to_and_return_from(DASHBOARD_URL)
    def get_daily_device_points(self):
        current_mobile_points = self.browser.get_value(AttributeType.XPath, DAILY_CURRENT_MOBILE_POINTS_XPATH)
        maximum_mobile_points = self.browser.get_value(AttributeType.XPath, DAILY_MAX_MOBILE_POINTS_XPATH).strip('/')
        return [current_mobile_points if current_mobile_points else -1, \
            maximum_mobile_points if maximum_mobile_points else -1]

    @convert_result_to_uint
    @go_to_and_return_from(DASHBOARD_URL)
    def get_daily_offer_points(self):
        current_offer_points = self.browser.get_value(AttributeType.XPath, DAILY_CURRENT_MOBILE_OFFER_POINTS_XPATH)
        maximum_offer_points = self.browser.get_value(AttributeType.XPath, DAILY_MAX_MOBILE_OFFER_POINTS_XPATH).strip('/')
        return [current_offer_points if current_offer_points else -1, \
            maximum_offer_points if maximum_offer_points else -1]