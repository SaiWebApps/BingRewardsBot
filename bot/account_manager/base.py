from browser_automation_utils.browser import AttributeType

# Constants
SIGN_IN_URL = 'https://www.bing.com/rewards/signin'
DASHBOARD_URL = 'https://www.bing.com/rewards/dashboard'

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
        self.browser.open(DASHBOARD_URL)

    def sign_in(self):
        '''
            @description
                Sign in to the specified Bing Rewards account.

            @return
                True if sign-in was successful, False otherwise
        '''
        self.browser.open(SIGN_IN_URL)
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