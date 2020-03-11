from datetime import date

import pandas as pd


class DataManager:
    def __init__(self):
        pass

    def generate_contest_report_to_csv(self, contest_participants_data, output_path, contest_name):
        print("Export Data to CSV FILE")
        df = pd.DataFrame(contest_participants_data)
        today = date.today()
        current_date = today.strftime("%b-%d-%Y")
        df.to_csv(output_path + contest_name + "_" + current_date + "_Report.csv", sep=",", index=False)
