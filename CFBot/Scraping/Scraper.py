from CFBot.Scraping.processes.ContestScraper import ContestScraper


class Scraper:
    def __init__(self, driver):
        self.__contest_scraper = ContestScraper(driver)

    def get_users_contest_standing_data(self):
        """ get users standing data for current contest.
        Args:
                None
        Returns:
                   List of dictionaries contains
                   each dictionary contains key [ handle,total solved,problem letter eg. A , B ,C ]
        """
        return self.__contest_scraper.get_users_contest_standing_data()
