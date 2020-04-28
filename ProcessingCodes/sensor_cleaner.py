# ------------------------------------------------------------------------------------------------
# Filename:
#        sensor_cleaner
# Author:
#        Jermy Thomas
#
# Description:
#        Code to clean sensor data and convert into a csv file with Date Stamps from
#        file creation time
#
# Credits:
#
# Requirements:
#      
#
# Notes:
#
# Todo:
#
# ------------------------------------------------------------------------------------------------
#
# Import <stuff>
import os
import pandas as pd
import fileinput
import datetime
import numpy as np

# Initialize list for creating timestamps from creation time
checktime = []

# Change directory to where the csv file is
print(os.getcwd())
os.chdir(r'<location_of_csv_files>')

# Name the headers for the updated csv file
my_cols = ['Empty', 'Time', 'Temperature', 'O', 'voltage', 'co2 conc',
           'Temp', 'Pressure', 'height above sea level', 'RH', 'Temp']

file = ('all other sensors')
filename = (file + '.csv')

# Find Creation Time
ctime = os.path.getctime(filename)
mtime = os.path.getmtime(filename)
print(mtime)


# convert csv into a dataframe
low = pd.read_csv(filename, sep=',', names=my_cols, skiprows=range(0, 2))

# Assign time difference between readings and create the timestamp list
Timedelta = pd.Timedelta(seconds=15)

#starttime = (datetime.datetime.fromtimestamp(ctime))

modtime = (datetime.datetime.fromtimestamp(mtime))
modtimenormal = modtime.replace(microsecond=0)

starttime = np.datetime64(modtimenormal) - (len(low)) * \
    np.timedelta64(15, 's') + 2*np.timedelta64(15, 's')

starttimenormal = starttime

for x in range(0, len(low)):
    newtime = np.datetime64(starttimenormal) + x*np.timedelta64(15, 's')
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
