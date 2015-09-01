from bingrewardsaccount import AccountCredentials
from bingrewardsbot import DesktopBingRewardsBot, MobileBingRewardsBot
from browser.webdrivermanager.browsertypes import BrowserType

def main():
    # Enter Hotmail/Outlook creds here.
    creds = []
    desktop_bot = DesktopBingRewardsBot(BrowserType.Chrome)
    desktop_bot.execute(creds, 30)
    desktop_bot.finish()

    mobile_bot = MobileBingRewardsBot(BrowserType.Chrome)
    mobile_bot.execute(creds, 20)
    mobile_bot.finish()

if __name__ == '__main__':
    main()
