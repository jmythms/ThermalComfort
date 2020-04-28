# ------------------------------------------------------------------------------------------------
# Filename:
#        combine_all
# Author:
#        Jermy Thomas
#
# Description:
#        Code to combine all data to one file
#
# Credits:
#
# Requirements:
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
import pathlib
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
import pandas_profiling as pp


# Counters
count10 = 0
count50 = 0
count110 = 0
countas = 0
countTS = 0


# Change directory to where the csv file is
rootdir = r'<location_of_sensor_data_directory>'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:

        if file == '10.csv_new.csv':
            os.chdir(os.path.join(subdir))
            print('Yahoo_10'+subdir)
            if count10 == 0:
                data10 = pd.read_csv('10.csv_new.csv', sep=',')
                data10.set_index('Datetime', inplace=True)
                data10 = data10[['Wind Speed', 'Air Temperature']]
                data10.columns = ['V_a_10', 'T_db_10']
            else:
                data10m = pd.read_csv('10.csv_new.csv', sep=',')
                data10m.set_index('Datetime', inplace=True)
                data10m = data10m[['Wind Speed', 'Air Temperature']]
                data10m.columns = ['V_a_10', 'T_db_10']
                data10 = pd.concat([data10, data10m])
            count10 = count10 + 1

        elif file == '50.csv_new.csv':
            os.chdir(os.path.join(subdir))
            print('Yahoo_50'+subdir)
            if count50 == 0:
                data50 = pd.read_csv('50.csv_new.csv', sep=',')
                data50.set_index('Datetime', inplace=True)
                data50 = data50[['Wind Speed', 'Air Temperature']]
                data50.columns = ['V_a_50', 'T_db_50']
            else:
                data50m = pd.read_csv('50.csv_new.csv', sep=',')
                data50m.set_index('Datetime', inplace=True)
                data50m = data50m[['Wind Speed', 'Air Temperature']]
                data50m.columns = ['V_a_50', 'T_db_50']
                data50 = pd.concat([data50, data50m])
            count50 = count50 + 1

        elif file == '110.csv_new.csv':
            os.chdir(os.path.join(subdir))
            print('Yahoo_110'+subdir)

            if count110 == 0:
                data110 = pd.read_csv('110.csv_new.csv', sep=',')
                data110.set_index('Datetime', inplace=True)
                data110 = data110[['Wind Speed', 'Air Temperature']]
                data110.columns = ['V_a_110', 'T_db_110']
            else:
                data110m = pd.read_csv('110.csv_new.csv', sep=',')
                data110m.set_index('Datetime', inplace=True)
                data110m = data110m[['Wind Speed', 'Air Temperature']]
                data110m.columns = ['V_a_110', 'T_db_110']
                data110 = pd.concat([data110, data110m])
            count110 = count110 + 1

        elif file == 'all other sensors.csv_new.csv':
            os.chdir(os.path.join(subdir))
            print('Yahoo_as'+subdir)

            if countas == 0:
                data_sensors = pd.read_csv('all other sensors.csv_new.csv', sep=',')
                data_sensors.set_index('Datetime', inplace=True)
                data_sensors = data_sensors[['Temperature', 'co2 conc',
                                             'Temp', 'Pressure', 'RH', 'Temp.1']]
            else:
                data_sensorsm = pd.read_csv('all other sensors.csv_new.csv', sep=',')
                data_sensorsm.set_index('Datetime', inplace=True)
                data_sensorsm = data_sensorsm[['Temperature', 'co2 conc',
                                               'Temp', 'Pressure', 'RH', 'Temp.1']]
                data_sensors = pd.concat([data_sensors, data_sensorsm])
            countas = countas + 1

# Code for getting data from Thermal Sensation
rootdir = r'<location_of_TS_data>'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filename = os.path.splitext(file)[0]
        name = filename.split("_ ", 1)[0]
        if name == '<participant_identifier>':
            os.chdir(os.path.join(subdir))
            print('TS Yahoo')

            if countTS == 0:
                date = filename.split("_ ", 1)[1]
                date = datetime.datetime.strptime(date, '%m-%d-%y').date()
                print(date)
                dataTS = pd.read_csv(file)
                dataTS['Date'] = date
                dataTS['Time'] = dataTS['Time'].apply(pd.to_datetime)
                dataTS['Time'] = pd.to_datetime(dataTS['Time'], format='%H:%M').dt.time
                dataTS['Datetime'] = dataTS[['Date', 'Time']].apply(
                    lambda x: ' '.join(x.dropna().astype(str).values), axis=1)
                dataTS.set_index('Datetime', inplace=True)
                clo = dataTS.iloc[0]['Clo']
                dataTS['Clo'] = clo
                dataTS = dataTS[['General Sensation', 'Activity', 'Clo']]

            else:
                date = filename.split("_ ", 1)[1]
                date = datetime.datetime.strptime(date, '%m-%d-%y').date()
                dataTSm = pd.read_csv(file)
                dataTSm['Date'] = date
                dataTSm['Time'] = dataTSm['Time'].apply(pd.to_datetime)
                dataTSm['Time'] = pd.to_datetime(dataTSm['Time'], format='%H:%M').dt.time
                dataTSm['Datetime'] = dataTSm[['Date', 'Time']].apply(
                    lambda x: ' '.join(x.dropna().astype(str).values), axis=1)
                dataTSm.set_index('Datetime', inplace=True)
                clo = dataTSm.iloc[0]['Clo']
                dataTSm['Clo'] = clo
                dataTSm = dataTSm[['General Sensation', 'Activity', 'Clo']]
                dataTS = pd.concat([dataTS, dataTSm])
            countTS = countTS + 1



combine = pd.merge(data10, data50, left_index=True, right_index=True)
# remove duplicate columns
combine = combine.loc[:, ~combine.columns.duplicated()]

combine = pd.merge(combine, data110, left_index=True, right_index=True)
# remove duplicate columns
combine = combine.loc[:, ~combine.columns.duplicated()]
combine = pd.merge(combine, data_sensors, left_index=True, right_index=True)

# remove duplicate columns
combine = combine.loc[:, ~combine.columns.duplicated()]
combine = pd.merge(combine, dataTS, left_index=True, right_index=True)
# remove duplicate columns
combine = combine.loc[:, ~combine.columns.duplicated()]

###################################################################
os.chdir(r'<location of HR data>')

dataHR = pd.read_csv('<HR_file_name>.csv', sep=',')
dataHR.set_index('Datetime', inplace=True)
dataHR = dataHR[['HR']]

combine = pd.merge(combine, dataHR, left_index=True, right_index=True)
print(combine)
# remove duplicate columns
combine = combine.loc[:, ~combine.columns.duplicated()]
# remove duplicate rows
combine.drop_duplicates(keep='first', inplace=True)

###################################################################
os.chdir(r'<location of Black globe data>')

dataBG = pd.read_csv('BG_final.csv', sep=',')
dataBG['Datetime_b'] = pd.to_datetime(dataBG['Datetime_b'], format='%m/%d/%Y %H:%M')
print(dataBG.dtypes)
dataBG.set_index('Datetime_b', inplace=True)
dataBG = dataBG[['BGTemp_C_Avg']]

combine = pd.merge(combine, dataBG, left_index=True, right_index=True)
combine = combine.loc[:, ~combine.columns.duplicated()]

###################################################################


combine['MRT'] = ((combine['BGTemp_C_Avg']+273) ** 4 + (2.5*10 ** 8)*combine['V_a_110']
                  * (combine['BGTemp_C_Avg']-combine['Temp.1'])) ** 0.25 - 273
print('MRT: ', combine['MRT'])

###################################################################

del combine['BGTemp_C_Avg']


os.chdir(r'<location_of_output_file>')



newfilename = ('<participant_identifier>'+'.csv')
combine.to_csv(newfilename)
