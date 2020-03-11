from CFBot.Navigation.Navigator import Navigator
from consts import *


class CFBotManager:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

        self.__driver = self.__set_up_driver()
        self.__navigator = Navigator(self.__driver)

    def get_contests_in_group_standing_data(self, group_name, contests_name):
        self.__navigator.login(self.__username, self.__password)
        put_human_delay(1)
        self.__navigator.move_to_group(COMMUNITY_GROUP, self.__username)

    def __set_up_driver(self):

        # set up chrome details
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        args = ["hide_console", ]

        if platform == "win32" or platform == "cygwin":
            # Windows Chrome lasted version 79
            driver = webdriver.Chrome("../data/drivers/chromedriverWindows.exe", chrome_options=chrome_options,
                                      service_args=args)
        elif platform == "linux":
            # LINUX OS
            driver = webdriver.Chrome("../data/drivers/chromedriverLinux", chrome_options=chrome_options,
                                      service_args=args)
        else:
            # MAC OS
            driver = webdriver.Chrome("../data/drivers/chromedriverMacOS", chrome_options=chrome_options,
                                      service_args=args)

        return driver


manager = CFBotManager(COMMUNITY_USER_NAME, COMMUNITY_PASSWORD)
manager.get_contests_in_group_standing_data(COMMUNITY_GROUP,
                                            ["Sheet #3 (Arrays)",
                                             "Weekly Contest #3",
                                             "Sheet #4 (String)",
                                             "Weekly Contest 4"])
