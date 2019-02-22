'''
File: process_crime_files.py
Author: Adam Pah
Description: 
Process the crime files to remove 'cidade', label the header, and add in commas
'''

#Standard path imports
from __future__ import division, print_function
import argparse
import glob
import os, sys

#Non-standard imports
import pandas as pd

#Global directories and variables

def main(args):
    header = ['State', 'City', 'Year', 'TotalPop', 'WhitePop', 'BlackPop', 'HispanicPop', 'NativePop', 'AsianPop']

    for fname in glob.glob('../../Data/Merged*csv'):
        lines = [l.strip().split(',') for l in open(fname).readlines()]
        newlines = []
        for line in lines:
            templine = []
            diff = len(header) - len(line)
            templine += line
            for i in range(diff):
                templine.append('')
            newlines.append(templine)
        #Create the dict for the dataframe
        pd_dict = {x:[] for x in header}
        for line in newlines:
            for j in range(len(line)):
                pd_dict[header[j]].append( line[j])
        df = pd.DataFrame(pd_dict)
        wfname = fname.split('/')[-1].split('Merged_')[-1]
        df.to_csv('../../Data/census/' + wfname, index = False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    args = parser.parse_args()
    main(args)
