import glob
from datetime import date

import pandas as pd
import csv


class DataManager:
    def __init__(self):
        pass

    def generate_contest_report_to_csv(self, contest_participants_data, output_path, contest_name):
        print("Export Data to CSV FILE")
        df = pd.DataFrame(contest_participants_data)
        today = date.today()
        current_date = today.strftime("%b-%d-%Y")
        df.to_csv(output_path + contest_name + "_" + current_date + "_Report.csv", sep=",", index=False)

    def make_2week_filtration(self, input_folder_path, output_path):
        keys = ["handle", "Training contest 1 # solved", "Training contest 2 # solved",
                "is participate Weekly contest1", "is participate Weekly contest2"]

        training_contest_number = 1
        weekly_contest_number = 3
        users_data = {}

        # get all handles
        for csv_file_name in glob.glob(input_folder_path + "/*.csv"):
            df = pd.read_csv(csv_file_name)
            df = df[['handle', 'total solved']]
            for index, row in df.iterrows():
                current_data = {"handle": row['handle'], "Training contest 1 # solved": 0,
                                "Training contest 2 # solved": 0,
                                "is participate Weekly contest1": 0, "is participate Weekly contest2": 0}

                users_data[row['handle']] = current_data

        # get users report
        for csv_file_name in glob.glob(input_folder_path + "/*.csv"):
            df = pd.read_csv(csv_file_name)
            df = df[['handle', 'total solved']]
            for index, row in df.iterrows():
                # if not weekly contest
                if "Weekly" not in csv_file_name:
                    users_data[row['handle']][keys[training_contest_number]] = int(row['total solved'])
                else:

                    users_data[row['handle']][keys[weekly_contest_number]] = 1

            if "Weekly" in csv_file_name:
                weekly_contest_number += 1
            else:
                training_contest_number += 1

        # convert dictionary of dictionaries to list of dictionaries
        ret = []
        for handle_name in users_data:
            ret.append(users_data[handle_name])

        # csv it to file
        df = pd.DataFrame(ret)
        today = date.today()
        current_date = today.strftime("%b-%d-%Y")
        df.to_csv(output_path + current_date + "Week_Report.csv", sep=",", index=False)

    def get_qualified_participant_from_filtration_week(self, csv_file_name, output_path):
        df = pd.read_csv(csv_file_name)

        df = df[(df['Training contest 1 # solved'] + df['Training contest 2 # solved'] >= 30)
                & ((df['is participate Weekly contest1'] == 1) | (df['is participate Weekly contest2'] == 1))]

        df.to_csv(output_path + "Qualifiers.csv", sep=",", index=False)


a = DataManager()
a.get_qualified_participant_from_filtration_week(
    "D:\work\ICPC_FCAI_Community_Automation\data\Reports\level1\\filteration2\Mar-11-2020Week_Report.csv",
    "D:\work\ICPC_FCAI_Community_Automation\\")
