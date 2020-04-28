import os
import pandas as pd
import fileinput
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


os.chdir(r'<directory_where_data_file_is_located (BG.csv)>')

file = ('BG')
filename = (file + '.csv')

BG = pd.read_csv(filename)


BG['BGTemp_C_Avg'] = pd.to_numeric(BG['BGTemp_C_Avg'], errors='coerce')

BG = BG[np.isfinite(BG['BGTemp_C_Avg'])]

BG['BGTemp_C_Avg'] = BG['BGTemp_C_Avg'].astype(str).astype(float)

BG['BALCK GLOBE DATE/TIME'] = BG['TIMESTAMP'].apply(pd.to_datetime)

BG['Year'] = BG['BALCK GLOBE DATE/TIME'].dt.year
BG['Month'] = BG['BALCK GLOBE DATE/TIME'].dt.month
BG['Date'] = BG['BALCK GLOBE DATE/TIME'].dt.day
BG['hour'] = BG['BALCK GLOBE DATE/TIME'].dt.hour
BG['Minute'] = BG['BALCK GLOBE DATE/TIME'].dt.minute

BG['Year'] = BG['Year'].astype(str).astype(int)
BG['Month'] = BG['Month'].astype(str).astype(int)
BG['Date'] = BG['Date'].astype(str).astype(int)
BG['hour'] = BG['hour'].astype(str).astype(int)
BG['Minute'] = BG['Minute'].astype(str).astype(int)


BG.columns = ['Timestamp', 'Record', 'BGTemp_C_Avg',
              'BALCK GLOBE DATE/TIME', 'Year', 'Month', 'Date', 'Hour',  'Minute']

BG.set_index('BALCK GLOBE DATE/TIME', inplace=True)
BG = BG.groupby([BG.index.month, BG.index.day, BG.index.hour, BG.index.minute]).mean()

BG = BG.astype({'Year': str, 'Month': str, 'Date': str, 'Hour': str,  'Minute': str})
BG['Date'] = BG[['Year', 'Month', 'Date']].apply(
    lambda x: '-'.join(x.dropna().astype(str).values), axis=1)
BG['Time'] = BG[['Hour', 'Minute']].apply(lambda x: ':'.join(x.dropna().astype(str).values), axis=1)
BG['Datetime'] = BG[['Date', 'Time']].apply(
    lambda x: ' '.join(x.dropna().astype(str).values), axis=1)
BG.drop(BG.columns.difference(['BGTemp_C_Avg', 'Datetime']), 1, inplace=True)
BG['Datetime'] = pd.to_datetime(BG['Datetime'], format="%Y-%m-%d %H:%M")

newfilename = (filename + '_new'+'.csv')
BG.to_csv(newfilename)
