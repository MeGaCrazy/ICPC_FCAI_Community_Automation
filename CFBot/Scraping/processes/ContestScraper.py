import string

from consts import *


class ContestScraper:
    def __init__(self, driver):
        self.__driver = driver

    def get_users_contest_standing_data(self):
        """ get users standing data for current contest.
        Args:
            None
        Returns:
            List of dictionaries contains
            each dictionary contains key [ handle,total solved,problem letter eg. A , B ,C ]
        """

        try:
            users_data = []
            problems_alphabetic_letters = list(string.ascii_uppercase)

            # first check unofficial button
            self.__check_button_show_unofficial()

            put_human_delay(1)
            participants_rows = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[@participantid]"))
            )

            # for each contest row
            for participant_row in participants_rows:
                current_participant_columns = participant_row.find_elements_by_css_selector("td")

                # if number of columns >=1
                if len(current_participant_columns) >= 4:

                    # get handle
                    handle_name = str(current_participant_columns[1].text).strip().replace("*", "")
                    handle_name = handle_name.strip().replace("#", "").strip()

                    # make dictionary to hold user data
                    current_user_data = {'handle': handle_name}
                    letter_idx, total_solved, total_tried = 0, 0, 0

                    # for each problem in contest
                    for i in range(4, len(current_participant_columns)):
                        # get its statue
                        current_problem_status = str(current_participant_columns[i].text).strip().split('\n')[0]

                        # if accept it
                        if "+" in current_problem_status:
                            total_solved += 1

                        # if tries
                        elif "-" in current_problem_status:
                            total_tried += 1
                        else:
                            pass

                        # add current problem statue with its letter to current_user_data dictionary
                        current_user_data[problems_alphabetic_letters[letter_idx]] = current_problem_status
                        letter_idx += 1

                    current_user_data['total solved'] = total_solved
                    current_user_data['total tried'] = total_tried

                    users_data.append(current_user_data)

            return users_data

        except WebDriverException:
            raise Exception("Can't participants rows")

    def __check_button_show_unofficial(self):
        """ check show unofficial button if not checked.

        :return: None
        """
        try:
            show_unofficial_button = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.ID, "showUnofficial"))
            )
            # if not check , then check it
            if not show_unofficial_button.is_selected():
                show_unofficial_button.click()

        except WebDriverException:
            raise Exception("Can't find unofficial button")
