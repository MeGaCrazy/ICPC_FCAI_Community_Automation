from consts import *


class Contest:
    def __init__(self, driver):
        self.__driver = driver

    def get_contest_link(self, contest_name):
        """ get the link of contest with given name

        Args:
            contest_name: string contains contest name
        Returns:
            string contains the link of the contest
        """
        try:

            contests_rows = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "highlighted-row"))
            )

            # for each contest row
            for contest_row in contests_rows:
                # get current row ( columns)
                current_contest_columns = contest_row.find_elements_by_css_selector("td")

                # if number of columns >=1
                if len(current_contest_columns) >= 4:
                    # if crawled contest name equal target contest name return the link
                    current_contest_name = str(current_contest_columns[0].text).split('\n')[0].lower().strip()

                    # if equal target contest name
                    if current_contest_name == contest_name.lower():
                        contest_link = current_contest_columns[3].find_element_by_css_selector("a"). \
                            get_attribute("href")

                        return contest_link

        except WebDriverException:
            raise Exception("Can't find contest link")

        return None
