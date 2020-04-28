# ------------------------------------------------------------------------------------------------
# Filename:
#        Atmos_cleaner
# Author:
#        Jermy Thomas
#
# Description:
#        Code to convert raw Atmos Data into a csv file with Date Stamps from
#        file creation time
#
# Credits:
#
# Requirements:
#        - Raw csv file
#
# Notes:
#
# Todo:
#
# ------------------------------------------------------------------------------------------------

# Import <stuff>
import os
import pandas as pd
import fileinput
import pathlib
import datetime
import numpy as np
import time
# Initialize list for creating timestamps from creation time
checktime = []

# Change directory to where the csv file is
print(os.getcwd())
os.chdir(r'<directory_location_where_file_is_stored (10.csv)>')


# Name the headers for the updated csv file
my_cols = ['Empty', 'Wind Speed', 'Wind Direction', 'Gust Wind Speed', 'Air Temperature',
           'x Orientation', 'Y Orientation', 'null', 'North Wind Speed', 'East Wind Speed']

file = ('10')
filename = (file + '.csv')

# Find Creation Time
f = open(filename)
line = f.readline()
f.close()
stime = line[34:53]
stime = time.strptime(stime, '%Y.%m.%d %H:%M:%S')
stime = datetime.datetime.fromtimestamp(time.mktime(stime))

mtime = os.path.getmtime(filename)

# Replace all - signs with commas
with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace('-', ','), end='')

# convert csv into a dataframe
low = pd.read_csv(filename, sep=',', names=my_cols, skiprows=1)

# Assign time difference between readings and create the timestamp list
Timedelta = pd.Timedelta(seconds=15)

modtime = (datetime.datetime.fromtimestamp(mtime))
modtimenormal = modtime.replace(microsecond=0)

divisor = (modtime-stime).total_seconds()/len(low)
print('divisor = ', divisor)
starttime = np.datetime64(modtimenormal) - len(low) / \
    (60/divisor) * np.timedelta64(1, 'm')

starttimenormal = starttime
print(starttime)
for x in range(0, len(low)):
    newtime = np.datetime64(starttimenormal) + x * \
        np.timedelta64(int(divisor * 10 ** 9), 'ns')
    checktime.append(newtime)

# Append datetime list to dataframe
low.insert(0, 'DateTimeNew', checktime)
del low['Empty']

verylow = low

# Create columns for date and time for later

verylow['Year'] = verylow['DateTimeNew'].dt.year
verylow['Month'] = verylow['DateTimeNew'].dt.month
verylow['Date'] = verylow['DateTimeNew'].dt.day
verylow['hour'] = verylow['DateTimeNew'].dt.hour
verylow['Minute'] = verylow['DateTimeNew'].dt.minute
verylow.set_index('DateTimeNew', inplace=True)
print(verylow.index.values[0:10])

# Nextstep is the averaging
newlow = verylow.groupby([verylow.index.day, verylow.index.hour, verylow.index.minute]).mean()

newlow = newlow.replace(r'\s+', np.nan, regex=True)
newlow = newlow.fillna(method='ffill')

# Create Datetime column again
newlow = newlow.astype({'Year': str, 'Month': str, 'Date': str, 'hour': str,  'Minute': str})
newlow['Date'] = newlow[['Year', 'Month', 'Date']].apply(
    lambda x: '-'.join(x.dropna().astype(str).values), axis=1)
newlow['Time'] = newlow[['hour', 'Minute']].apply(
    lambda x: ':'.join(x.dropna().astype(str).values), axis=1)
newlow['Datetime'] = newlow[['Date', 'Time']].apply(
    lambda x: ' '.join(x.dropna().astype(str).values), axis=1)
Datetime = pd.to_datetime(newlow['Datetime'], format="%Y-%m-%d %H:%M")
newlow.drop(labels=['Datetime'], axis=1, inplace=True)
newlow.insert(0, 'Datetime', Datetime)

# create final file

newfilename = (filename + '_new'+'.csv')
newlow.to_csv(newfilename)
