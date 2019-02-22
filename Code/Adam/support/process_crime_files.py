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
    for fname in glob.glob('../../Data/cidade*csv'):
        df = pd.read_csv(fname, sep=' ', header =None, names= ['Year', 'Murders', 'Robbery', 'Assault', 'Burglary'])
        wfname = fname.split('/')[-1].split('estado_')[-1]
        df.to_csv('../../Data/crime/' + wfname, index = False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    args = parser.parse_args()
    main(args)
