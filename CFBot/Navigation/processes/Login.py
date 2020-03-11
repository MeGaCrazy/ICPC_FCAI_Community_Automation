

from consts import *


class Login:

    def __init__(self, driver):
        self.__driver = driver

    def start(self, user_name, password):
        # open site link

        self.__driver.get(ONLINE_JUDGE_LINK)
        put_human_delay(1)

        # fill user name
        self.__fill_user_name(user_name)

        # fill password
        self.__fill_password(password)

        put_human_delay(.3)
        # click remember for a month button
        self.__check_remember_for_month_button()

        put_human_delay(.3)
        # click Login button
        self.__click_login_button()

    def __fill_user_name(self, user_name):
        try:

            user_name_text_filed = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.ID, "handleOrEmail"))
            )

            for character in user_name:
                user_name_text_filed.send_keys(character)
                put_human_delay(.15)
        except WebDriverException:
            raise Exception("Can't Find Username Text Field")

    def __fill_password(self, password):
        try:
            # get the next button
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )

            for character in password:
                element.send_keys(character)
                sleep(.15)
        except WebDriverException:
            raise Exception("Can't find password text field")

    def __check_remember_for_month_button(self):
        try:
            # get the check button
            check_button = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.ID, "remember")))

            check_button.click()
        except WebDriverException:
            raise Exception("Can't find check remember me button")

    def __click_login_button(self):
        try:
            # get the login button
            login_button = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "submit"))
            )

            login_button.click()
        except WebDriverException:
            raise Exception("Can't find login button")
