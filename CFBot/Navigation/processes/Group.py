from consts import *


class Group:
    def __init__(self, driver):
        self.__driver = driver

    def move_to_groups_page(self, username):
        self.__driver.get(GROUP_TEMPLATE_LINK + username)

    def move_to_group(self, group_name):
        try:

            group_links = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "groupName"))
            )
            for group_link in group_links:
                if str(group_link.text).strip() == group_name.strip():
                    group_link.click()
                    return

        except WebDriverException:
            raise Exception("Can't Click on group name")
