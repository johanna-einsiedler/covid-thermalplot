#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 20:41:57 2021

@author: johanna
"""

import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--inputdir', default='../data_downloads/')
parser.add_argument('--outputdir', default='../data_transformed/')
parser.add_argument('--variable')
parser.add_argument('--file', default="0")

args = parser.parse_args()

if args.file == '0':
    csv_name = 'time_series_covid19_'+str(args.variable)+'_global.csv'
else:
    csv_name = args.file

# read in data
df = pd.read_csv(args.inputdir + csv_name)

# delete lat and long columns
df = df.drop([ 'Lat', 'Long'], axis = 1)

# group data when provided on a province/state level
df[df.columns.difference(['Province/State', 'Country/Region'])] = df[df.columns.difference(['Province/State', 'Country/Region'])].apply(pd.to_numeric,errors='coerce')
df =  df.fillna(-1)
df = df.groupby('Country/Region').sum()
df['country'] = df.index



# transform from wide to long
df = pd.melt(df, id_vars ='country')

# rename columns
df.columns = ['country','date', 'count']


# save output
output_path = args.outputdir + 'data_'+ args.variable+'.csv'
df.to_csv(output_path)

print('Saved as: ' + output_path)