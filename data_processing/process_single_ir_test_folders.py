"""
Script to analyze a directory of cell data.
Directory should be organized as:

SELECTED DIRECTORY
----> 1 (cell number, folder)
--------> logs (test logs, folder)
--------> 1 Continuous_Step_Cycles Rest 2023-03-08 19-41-54 (Rest test data, file)
--------> 1 Continuous_Step_Cycles Single_IR_Test 2023-03-08 19-41-55 (IR test data, file)
--------> ANY OTHER FUTURE TEST DATA FOR CELL 1
----> 2
--------> ...
----> 3
--------> ...
----> ...

Calculated data will be saved to a csv file named "Processed Data.csv".
"""


import csv
import os
import shutil
import re
from tkinter.filedialog import askdirectory

import pandas as pd

# Function borrowed from Micah's GraphIV.py module, with a small edit.
def process_single_ir_test(df, printout = False):
    """
    Calculates the internal resistance for a single IR test data file.
    Mostly copied from Micah's GraphIV.py module, with a small edit
    to ignore the very first voltage and current measurement if possible.
    """
    #find index of last extry in first step
    #Data_Timestamp_From_Step_Start goes from high back to low - diff is negative.
    df['step_time_diff_single_step'] = df['Data_Timestamp_From_Step_Start'].diff().fillna(0)
    row_index_2nd_step = df['step_time_diff_single_step'].argmin()

    #split data into 1st step and 2nd step
    df_1 = df.iloc[:row_index_2nd_step]
    df_2 = df.iloc[row_index_2nd_step:]

    # Ignore first reading in case current draw hasn't reached the set current yet.
    if len(df_1['Voltage']) > 1:
        s1_v = df_1['Voltage'][1:].mean()
        s1_i = df_1['Current'][1:].mean()
    else:
        s1_v = df_1['Voltage'][1:].mean()
        s1_i = df_1['Current'][1:].mean()

    if len(df_2['Voltage']) > 1:
        s2_v = df_2['Voltage'][1:].mean()
        s2_i = df_2['Current'][1:].mean()
    else:
        s2_v = df_2['Voltage'].mean()
        s2_i = df_2['Current'].mean()

    #r = v/i
    dc_ir = (s2_v - s1_v) / (s2_i - s1_i)
    if printout:
        print(f"Internal Resistance: {dc_ir} Ohms, {dc_ir*1000} mOhms")

    return dc_ir

if __name__ == "__main__":
    folder = askdirectory(title='Select Folder') # shows dialog box and return the path

    subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]
    new_folder = os.path.join(folder, "Aggregated Data")

    if not os.path.exists(new_folder):
        os.mkdir(new_folder)

    for sub in subfolders:
        for f in os.listdir(sub):
            if ".csv" in f and "Processed Data" not in f:
                src = os.path.join(sub, f)
                dst = os.path.join(new_folder , f.replace("Continuous_Step_Cycles ", ""))
                if not os.path.exists(dst):
                    shutil.copy(src, dst)

    cell_dict = {}

    files = [f for f in os.scandir(new_folder) if os.path.isfile(f)]

    for file in files:
        df = pd.read_csv(file)
        file_name, ext = os.path.splitext(file)
        file_name = file_name.split()
        cell_num = int(re.sub(r'\D', '', file_name[-4]))
        test_type = file_name[-3]
        if cell_num not in cell_dict:
            cell_dict[cell_num] = {
                "DC IR": 0,
                "OCV": 0,
            }

        if test_type == "Single_IR_Test":
            cell_dict[cell_num]["DC IR"] = process_single_ir_test(df)
        elif test_type == "Rest":
            cell_dict[cell_num]["OCV"] = df['Voltage'][0]


    cell_dict = dict(sorted(cell_dict.items()))

    processed_data_file = os.path.join(folder, "Processed Data.csv")
    with open(processed_data_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Cell Number", "Internal Resistance [Ohms]", "Open Circuit Voltage [V]"])
        for cell, data in cell_dict.items():
            writer.writerow([cell, data["DC IR"], data["OCV"]])

    print(f"Finished. Data in {processed_data_file}")
