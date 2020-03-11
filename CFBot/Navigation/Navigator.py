from time import sleep

from CFBot.Navigation.processes.Group import Group
from CFBot.Navigation.processes.Login import Login
from consts import *


class Navigator:
    def __init__(self, driver):
        self.__login_navigator = Login(driver)
        self.__group_navigator = Group(driver)

    def login(self, user_name, password):
        self.__login_navigator.start(user_name, password)

    def move_to_group(self, group_name, user_name):
        self.__group_navigator.move_to_groups_page(user_name)
        put_human_delay(1)
        self.__group_navigator.move_to_group(group_name)
