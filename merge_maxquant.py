import numpy as np
import pandas as pd
import sys
import argparse

# shut off settingwithcopy warning
pd.options.mode.chained_assignment = None  # default='warn'

"""
Purpose: Merges Mix 1 and Mix 2 proteinGroups.txt files generated from MaxQuant.

To use:
python merge_maxquant.py -m1 <path/to/file> -m2 <path/to/file> --prefix <string>
Example:
python merge_maxquant.py -m1 LM1C/proteinGroups.txt -m2 LM2C/proteinGroups.txt --prefix Mix12_Con

Paramters:
Required:
-m1: proteinGroups.txt file for Mix 1
-m2: proteinGroups.txt file for Mix 2
Optional:
--prefix: prefix for output file name
"""
__author__ = "Sara Jones"
__email__ = "jonessarae@gmail.com"
__doc__ = "Merges Mix 1 and Mix 2 proteinGroups.txt files from MaxQuant."


def main(args):

    # first mix file
    first_file = args.m1
    # second mix file
    second_file = args.m2

    # read in files for Mix 1 and Mix 2
    first_df = pd.read_csv(first_file, sep="\t")
    second_df = pd.read_csv(second_file, sep="\t")

    try:
        # intensity columns of first and second mix
        first_intensity_df = first_df[first_df.filter(regex="Majority protein IDs|Intensity H |Intensity M |Intensity L ").columns]
        second_intensity_df = second_df[second_df.filter(regex="Majority protein IDs|Intensity H |Intensity M |Intensity L ").columns]
    except KeyError:
        print("At least one of the files is not a proteinGroups.txt.")
        print("Please check the paths to the files.")

    m1_stim = first_intensity_df.columns[1].split(" ")[2].split("_")[0][0] # ex. L for LPS
    m2_stim = second_intensity_df.columns[1].split(" ")[2].split("_")[0][0]
    m1_group = first_intensity_df.columns[1].split(" ")[2].split("_")[0][3] # ex. C for control
    m2_group = second_intensity_df.columns[1].split(" ")[2].split("_")[0][3]
    m1_mix = first_intensity_df.columns[1].split(" ")[2].split("_")[0][2] # ex. 1 for Mix 1
    m2_mix = second_intensity_df.columns[1].split(" ")[2].split("_")[0][2]

    if m1_stim != m2_stim:
        print("The proteinGroups.txt files do not belong to the same condition.")
        print("Please check the paths to the files.")
        sys.exit(0) # exit program

    if m1_group != m2_group:
        print("The proteinGroups.txt files do not belong to the same group.")
        print("Please check the paths to the files.")
        sys.exit(0) # exit program

    if m1_mix == m2_mix:
        print("The proteinGroups.txt files belong to the same mix.")
        print("Please check the path to the file for each mix.")
        sys.exit(0) # exit program

    # get all unique protein hits from both mix files
    df_rows = pd.concat([first_df[["Majority protein IDs"]], second_df[["Majority protein IDs"]]], ignore_index=True)
    df_rows = df_rows[["Majority protein IDs"]].drop_duplicates()
    df_rows = df_rows.sort_values(by="Majority protein IDs")
    df_rows = df_rows.reset_index(drop=True)

    # list of non-intensity columns to keep
    col_list = ["Majority protein IDs", "Protein names", "Gene names", "Fasta headers", "Peptides",
            "Unique peptides", "Sequence coverage [%]", "Mol. weight [kDa]","Sequence length",
            "Q-value", "Score", "Only identified by site", "Reverse", "Potential contaminant"]

    first_info_df = first_df[col_list] # dataframe of first mix with non-intensity columns
    second_info_df = second_df[col_list] # dataframe of second mix with non-intensity columns

    # merge first and second mix dataframes with temp dataframe on unique protein hits
    temp_df = pd.merge(df_rows, first_info_df, how="left", on="Majority protein IDs")
    temp_df = pd.merge(temp_df, second_info_df, how="left", on="Majority protein IDs")

    # create new df to combine first and second info columns
    new_df = temp_df[["Majority protein IDs"]]
    # number of columns in dataframe to iterate through
    length = int((len(temp_df.columns))/2)+1
    # iterate through specific columns
    for i in range(1, length):
        col_name = temp_df.columns[i][:-2] # column name
        x_name =col_name + "_x" # first mix column
        y_name = col_name + "_y" # second mix column
        # if data type of column contains numbers
        if temp_df[temp_df.columns[i]].dtype == np.float64:
            if temp_df.columns[i] is "Q-value_x":
                # get min value of Q-value between two mixes
                new_df[col_name] = temp_df[[x_name, y_name]].min(axis=1)
            else:
                # get max value between two mixes
                new_df[col_name] = temp_df[[x_name, y_name]].max(axis=1)
        else:
            # fill NaN values between two mixes of each column
            new_df[col_name] = temp_df[[x_name, y_name]].bfill(axis=1).iloc[:, 0]


    # merge intensity dataframes to new dataframe
    new_df = pd.merge(new_df, first_intensity_df, how="left", on="Majority protein IDs")
    new_df = pd.merge(new_df, second_intensity_df, how="left", on="Majority protein IDs")

    # replace any NaN values with 0 for intensity columns
    new_df[new_df.columns[14:]] = new_df[new_df.columns[14:]].replace(np.nan, 0)

    # save to txt file
    if args.prefix:
        new_df.to_csv(args.prefix + "_proteinGroups.txt", sep="\t", index=False)
    else:
        new_df.to_csv("proteinGroups.txt", sep="\t", index=False)

if __name__ == "__main__":

    # create arguments
    p = argparse.ArgumentParser(description=__doc__, prog="merge_maxquant.py",
        usage="%(prog)s -m1 <path/to/file> -m2 <path/to/file> [options]", add_help=True)
    p.add_argument("-m1", help="path to experiment proteinGroups.txt file", required=True)
    p.add_argument("-m2", help="path to control proteinGroups.txt file", required=True)
    p.add_argument("--prefix", help="prefix to use for naming output file")

    # parse arguments
    args = p.parse_args()
    # run program with arguments
    main(args)
