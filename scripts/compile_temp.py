# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 15:05:54 2015

@author: Christopher M. Tasich
@organization: Vanderbilt University
"""
#%% Import packages

import csv,os,re
import difflib as dl
import datetime as dt
import time

#%% Initialize variables

station_data = {}

#%% Import station list

fn = ['STN-ID','STN-NAME','DISTRICT','LAT','LON','ELEVATION (Meters)',
      'BEGIN-DATE','END-DATE']
stations = r'D:\Windows\Users\tasichcm\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\stations.csv'
with open(stations) as f:
    reader = csv.DictReader(f,fieldnames=fn)
    for row in reader:
        station_data[row['STN-NAME']] = row
        station_data[row['STN-NAME']].pop('STN-NAME')
        
#%% Import daily temp data

dir = r'D:\Windows\Users\tasichcm\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\Daily\Temp'
files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]

fn = ['ST-NAME','LAT','LON','ELEVATION','TEMP_MAX','TEMP_MIN','UNIT']
all_data={}
for file in files:
    station = file[:-19]
    temp={}
    temp_data = dict.fromkeys(fn)
    with open(os.path.join(dir,file)) as f:
        reader = csv.DictReader(f)
        header = [next(f) for x in xrange(4)]
        header = map(str.strip,header)
        header_xyz = header[1].split()
        temp_data['ST-NAME'] = header[0]
        temp_data['LAT'] = header_xyz[1]
        temp_data['LON'] = header_xyz[3]
        temp_data['ELEVATION'] = header_xyz[5]
        temp_data['UNIT'] = header[3]
        if 'max' in header[2]:
           for row in reader:
               date = dt.date.fromtimestamp(time.mktime(time.strptime(
               row['Date'],"%Y-%m-%d")))
               temp[date] = row['Temp.max']
           temp_data['TEMP_MAX'] = temp
           type = 'TEMP_MAX'
        elif 'min' in header[2]:
            for row in reader:
                date = dt.date.fromtimestamp(time.mktime(time.strptime(
                row['Date'],"%Y-%m-%d")))
                temp[date] = row['Temp.min']
            temp_data['TEMP_MIN'] = temp
            type = 'TEMP_MIN'
        if not station in all_data.keys():
            all_data[station] = temp_data
        else:
            all_data[station][type] = temp_data[type]
        
#%% Compare temp stations to station list

names1=[]
names2=[]
names3=[]
close_name=[]
bad=[]
count=0

for station in all_data.keys():
    names1.append(station.upper())
    close_name = dl.get_close_matches(names1[count],station_data.keys(),1,0.9)
    if not close_name:
        close_name = ['none']
    if r'(' in file[:-17]:
        names2.append(re.findall(r'\(([^\)]+)\)',station.upper())[0] + ' ESTATE')
        names3.append(re.findall(r'^[^\(]+',station.upper())[0].strip())
    else:
        names2.append('NA')
        names3.append('NA')
    if names1[count] in station_data.keys():
        all_data[station]['STN-ID'] = station_data[names1[count]]['STN-ID']
        all_data[station]['LAT'] = station_data[names1[count]]['LAT']
        all_data[station]['LON'] = station_data[names1[count]]['LON']
        all_data[station]['BEGIN-DATE'] = station_data[names1[count]]['BEGIN-DATE']
        all_data[station]['END-DATE'] = station_data[names1[count]]['END-DATE']
        all_data[station]['ELEVATION'] = station_data[names1[count]]['ELEVATION (Meters)']
        all_data[station]['MATCH'] = names1[count]
        all_data[station]['MATCH-TYPE'] = 'names1'
    elif names2[count] in station_data.keys():
        all_data[station]['STN-ID'] = station_data[names2[count]]['STN-ID']
        all_data[station]['LAT'] = station_data[names2[count]]['LAT']
        all_data[station]['LON'] = station_data[names2[count]]['LON']
        all_data[station]['BEGIN-DATE'] = station_data[names2[count]]['BEGIN-DATE']
        all_data[station]['END-DATE'] = station_data[names2[count]]['END-DATE']
        all_data[station]['ELEVATION'] = station_data[names2[count]]['ELEVATION (Meters)']
        all_data[station]['MATCH'] = names2[count]
        all_data[station]['MATCH-TYPE'] = 'names2'
    elif names3[count] in station_data.keys():
        all_data[station]['STN-ID'] = station_data[names3[count]]['STN-ID']
        all_data[station]['LAT'] = station_data[names3[count]]['LAT']
        all_data[station]['LON'] = station_data[names3[count]]['LON']
        all_data[station]['BEGIN-DATE'] = station_data[names3[count]]['BEGIN-DATE']
        all_data[station]['END-DATE'] = station_data[names3[count]]['END-DATE']
        all_data[station]['ELEVATION'] = station_data[names3[count]]['ELEVATION (Meters)']
        all_data[station]['MATCH'] = names3[count]
        all_data[station]['MATCH-TYPE'] = 'names3'
    elif close_name[0] in station_data.keys():
        all_data[station]['STN-ID'] = station_data[close_name[0]]['STN-ID']
        all_data[station]['LAT'] = station_data[close_name[0]]['LAT']
        all_data[station]['LON'] = station_data[close_name[0]]['LON']
        all_data[station]['BEGIN-DATE'] = station_data[close_name[0]]['BEGIN-DATE']
        all_data[station]['END-DATE'] = station_data[close_name[0]]['END-DATE']
        all_data[station]['ELEVATION'] = station_data[close_name[0]]['ELEVATION (Meters)']
        all_data[station]['MATCH'] = close_name[0]
        all_data[station]['MATCH-TYPE'] = 'close_match'
    else:
        bad.append(station)
    count = count + 1

#%% Export data to csv

fn = ['STN-ID','ST-NAME','LAT','LON','DATE','TEMP_MAX','TEMP_MIN']

with open(r'D:\Windows\Users\tasichcm\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\Daily\daily_temp.csv','wb') as f:
    writer = csv.DictWriter(f,fieldnames=fn)
    writer.writeheader()
    for station in all_data.keys():
        for date in sorted(all_data[station]['TEMP_MAX'].keys()):
            writer.writerow({'STN-ID':all_data[station]['STN-ID'],
            'ST-NAME':all_data[station]['ST-NAME'],
            'LAT':all_data[station]['LAT'],'LON':all_data[station]['LON'],
            'DATE':date,'TEMP_MAX':all_data[station]['TEMP_MAX'][date],'TEMP_MIN':all_data[station]['TEMP_MIN'][date]})