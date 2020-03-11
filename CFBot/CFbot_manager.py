from CFBot.DataManagement.DataManager import DataManager
from CFBot.Navigation.Navigator import Navigator
from CFBot.Scraping.Scraper import Scraper
from consts import *


class CFBotManager:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

        self.__driver = self.__set_up_driver()
        self.__navigator = Navigator(self.__driver)
        self.__scraper = Scraper(self.__driver)
        self.__data_manager = DataManager()

    def generate_contests_in_group_standing_data(self, group_name, contests_name, output_path):
        self.__navigator.login(self.__username, self.__password)
        put_human_delay(1)
        self.__navigator.move_to_group(group_name, self.__username)
        contests_link = self.__navigator.get_contests_links_in_group(contests_name)
        put_human_delay(1)

        contest_idx = 0
        # for each contest link
        for contest_link in contests_link:
            # Open a new window
            self.__driver.execute_script("window.open('');")

            # switch to the new window
            self.__driver.switch_to.window(self.__driver.window_handles[len(self.__driver.window_handles) - 1])

            put_human_delay(.3)

            # go to contest link
            self.__driver.get(contest_link)

            # get participants data
            contest_participants_data = self.__scraper.get_users_contest_standing_data()

            self.__data_manager.generate_contest_report_to_csv(contest_participants_data,
                                                               output_path, contests_name[contest_idx])

            contest_idx += 1

            # close current windows
            self.__driver.close()
            self.__driver.switch_to.window(self.__driver.window_handles[len(self.__driver.window_handles) - 1])

    def __set_up_driver(self):

        # set up chrome details
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        args = ["hide_console", ]

        if platform == "win32" or platform == "cygwin":
            # Windows Chrome lasted version 79
            driver = webdriver.Chrome("../data/drivers/chromedriverWindows.exe",
                                      service_args=args)
        elif platform == "linux":
            # LINUX OS
            driver = webdriver.Chrome("../data/drivers/chromedriverLinux",
                                      service_args=args)
        else:
            # MAC OS
            driver = webdriver.Chrome("../data/drivers/chromedriverMacOS",
                                      service_args=args)

        return driver


manager = CFBotManager(COMMUNITY_USER_NAME, COMMUNITY_PASSWORD)
manager.generate_contests_in_group_standing_data(COMMUNITY_GROUP,
                                                 ["Weekly Contest 4", "Sheet #3 (Arrays)",
                                                  "Weekly Contest #3",
                                                  "Sheet #4 (String)"
                                                  ], FILTERATION2_PATH)
