import string

from consts import *


class ContestScraper:
    def __init__(self, driver):
        self.__driver = driver

    def get_users_contest_standing_data(self):
        """ get users standing data for current contest.
             Taking in consideration don't count Admins
             if there's multiple page
        Args:
            None
        Returns:
            List of dictionaries contains
            each dictionary contains key [ handle,total solved,problem letter eg. A , B ,C ]
        """

        try:
            users_data = {}
            problems_alphabetic_letters = list(string.ascii_uppercase)
            # first check unofficial button
            self.__check_button_show_unofficial()
            sleep(1)
            first = True
            pages = []
            try:
                pages = self.__driver.find_elements_by_class_name("page-index")
            except Exception:
                pass
            if pages is None or len(pages) == 0:
                pages = ["12"]

            for page_index in pages:
                if not first:
                    href = page_index.find_element_by_css_selector("a").get_attribute("href")
                    self.__driver.get(href)

                first = False

                print("Start Crawling ")

                put_human_delay(1)
                participants_rows = WebDriverWait(self.__driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tr[@participantid]"))
                )

                self.__driver.implicitly_wait(0)
                idx = 0
                # for each contest row
                for participant_row in participants_rows:

                    current_participant_columns = participant_row.find_elements_by_css_selector("td")

                    # if number of columns >=1
                    if len(current_participant_columns) >= 4:

                        # get handle
                        handle_name = str(current_participant_columns[1].text).strip()

                        # ignore ADMIN
                        if "*" not in handle_name and "to practice" not in handle_name:
                            continue

                        handle_name = handle_name.replace("*", "")
                        handle_name = handle_name.strip().replace("#", "").strip()
                        handle_name = handle_name.split(' ')[0]

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

                        print("Finished Crawling participants", idx + 1)
                        idx += 1

                        # if data already exists
                        if handle_name in users_data:
                            
                            for key in current_user_data.keys():
                                current_problem_status = current_user_data[key]

                                if len(key) == 1 and 'A' <= key <= 'Z':
                                    if "+" in current_problem_status and "+" not in users_data[handle_name][key]:
                                        users_data[handle_name]['total solved'] += 1
                                        users_data[handle_name][key] = current_problem_status
                        else:
                            users_data[handle_name] = current_user_data

            ret = []
            for handle_name in users_data:
                ret.append(users_data[handle_name])

            print("End Crawling")
            return ret

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
