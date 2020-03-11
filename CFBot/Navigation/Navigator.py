from time import sleep

from CFBot.Navigation.processes.Contest import Contest
from CFBot.Navigation.processes.Group import Group
from CFBot.Navigation.processes.Login import Login
from consts import *


class Navigator:
    def __init__(self, driver):
        self.__login_navigator = Login(driver)
        self.__group_navigator = Group(driver)
        self.__contest_navigator = Contest(driver)

    def login(self, user_name, password):
        self.__login_navigator.start(user_name, password)

    def move_to_group(self, group_name, user_name):
        self.__group_navigator.move_to_groups_page(user_name)
        put_human_delay(1)
        self.__group_navigator.move_to_group(group_name)

    def get_contests_links_in_group(self, contests_name):
        """ get links of the contests of given name
        Args:
           contests_name: list of strings contains contest name
        Returns:
           List of strings contains contests links
        """
        contests_link = []
        for contest_name in contests_name:
            cur_contest_link = self.__contest_navigator.get_contest_link(contest_name)
            if cur_contest_link is not None:
                contests_link.append(cur_contest_link)

        return contests_link
