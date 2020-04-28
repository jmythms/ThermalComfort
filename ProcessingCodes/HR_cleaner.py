import os
import pandas as pd
import fileinput
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

os.chdir(r'<location_of_hr_file>')

file = ('<HR_file_name>')
filename = (file + '.csv')
HR1 = []
HR = pd.read_csv(filename)

HR['HEART RATE DATE/TIME'] = HR['HEART RATE DATE/TIME'].apply(pd.to_datetime)

HR['Year'] = HR['HEART RATE DATE/TIME'].dt.year
HR['Month'] = HR['HEART RATE DATE/TIME'].dt.month
HR['Date'] = HR['HEART RATE DATE/TIME'].dt.day
HR['hour'] = HR['HEART RATE DATE/TIME'].dt.hour
HR['Minute'] = HR['HEART RATE DATE/TIME'].dt.minute

HR['Year'] = HR['Year'].astype(str).astype(int)
HR['Month'] = HR['Month'].astype(str).astype(int)
HR['Date'] = HR['Date'].astype(str).astype(int)
HR['hour'] = HR['hour'].astype(str).astype(int)
HR['Minute'] = HR['Minute'].astype(str).astype(int)


HR.set_index('HEART RATE DATE/TIME', inplace=True)
HR = HR.groupby([HR.index.month, HR.index.day, HR.index.hour, HR.index.minute]).mean()

HR.columns = ['HR', 'Year', 'Month', 'Date', 'Hour',  'Minute']
HR = HR.astype({'Year': str, 'Month': str, 'Date': str, 'Hour': str,  'Minute': str})
HR['Date'] = HR[['Year', 'Month', 'Date']].apply(
    lambda x: '-'.join(x.dropna().astype(str).values), axis=1)
HR['Time'] = HR[['Hour', 'Minute']].apply(
    lambda x: ':'.join(x.dropna().astype(str).values), axis=1)
HR['Datetime'] = HR[['Date', 'Time']].apply(
    lambda x: ' '.join(x.dropna().astype(str).values), axis=1)
HR.drop(HR.columns.difference(['HR', 'Datetime']), 1, inplace=True)
HR['Datetime'] = pd.to_datetime(HR['Datetime'], format="%Y-%m-%d %H:%M")
print(HR)

newfilename = (filename + '_new'+'.csv')
HR.to_csv(newfilename)
