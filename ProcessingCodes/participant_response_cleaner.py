import os
import pandas as pd
import fileinput
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

os.chdir(r'<directory_location>')

path, filename = os.path.split(
    r"<directory_location>\<participant_identifier>_ <date>.csv")
file = os.path.splitext(filename)[0]
date = file.split("_ ", 1)[1]
print(file.split("_ ", 1)[0])


date = datetime.datetime.strptime(date, '%m-%d-%y').date()

data = pd.read_csv(filename)
data['Date'] = date
data['Time'] = data['Time'].apply(pd.to_datetime)
data['Time'] = pd.to_datetime(data['Time'], format='%H:%M').dt.time
print(data['Time'])
data['Datetime'] = data[['Date', 'Time']].apply(
    lambda x: ' '.join(x.dropna().astype(str).values), axis=1)

data['Datetime'] = pd.to_datetime(data['Datetime'], format="%Y-%m-%d %H:%M")
print(data)


newfilename = (filename + '_new'+'.csv')
data.to_csv(newfilename)
