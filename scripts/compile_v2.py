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

fn = ['STN-ID','STN-NAME','DISTRICT','LAT','LON','ELEVATION (Meters)','BEGIN-DATE','END-DATE']
stations = r'D:\Windows\Users\tasichcm\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\stations.csv'
with open(stations) as f:
    reader = csv.DictReader(f,fieldnames=fn)
    for row in reader:
        station_data[row['STN-NAME']] = row
        station_data[row['STN-NAME']].pop('STN-NAME')
        
#%% Import daily precip data

dir = r'D:\Windows\Users\tasichcm\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\Daily\Precip'
files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]

fn = ['ST-NAME','LAT','LON','ELEVATION','PRECIP','UNIT']
all_data={}
max_date=dt.date(1800,1,1)
min_date=dt.date(2100,1,1)
for file in files:
    precip={}
    precip_data = dict.fromkeys(fn)
    with open(os.path.join(dir,file)) as f:
        line1 = f.readline().strip()
        f.seek(0)
        reader = csv.DictReader(f)
        if line1 == 'Millimeters':
            header = [next(f) for x in xrange(1)]
            header = map(str.strip,header)
            precip_data['ST-NAME'] = 'NA'
            precip_data['LAT'] = 'NA'
            precip_data['LON'] = 'NA'
            precip_data['ELEVATION'] = 'NA'
            precip_data['UNIT'] = header[0]
            for row in reader:
                precip[dt.date.fromtimestamp(time.mktime(time.strptime(
                row['Date'],"%Y-%m-%d")))] = row['None']
        else:
            header = [next(f) for x in xrange(4)]
            header = map(str.strip,header)
            header_xyz = header[1].split()
            precip_data['ST-NAME'] = header[0]
            precip_data['LAT'] = header_xyz[1]
            precip_data['LON'] = header_xyz[3]
            precip_data['ELEVATION'] = header_xyz[5]
            precip_data['UNIT'] = header[3]
            for row in reader:
                date = dt.date.fromtimestamp(time.mktime(time.strptime(
                row['Date'],"%Y-%m-%d")))
                precip[date] = row['Precip']
                if date >= max_date:
                    max_date = date
                elif date < min_date:
                    min_date = date
        precip_data['PRECIP'] = precip
        all_data[file] = precip_data
        
#%% Compare precip stations to station list

names1=[]
names2=[]
names3=[]
close_name=[]
bad=[]
count=0

for file in all_data.keys():
    names1.append(file[:-17].upper())
    close_name = dl.get_close_matches(names1[count],station_data.keys(),1,0.9)
    if not close_name:
        close_name = ['none']
    if r'(' in file[:-17]:
        names2.append(re.findall(r'\(([^\)]+)\)',file[:-17].upper())[0] + ' ESTATE')
        names3.append(re.findall(r'^[^\(]+',file[:-17].upper())[0].strip())
    else:
        names2.append('NA')
        names3.append('NA')
    if names1[count] in station_data.keys():
        all_data[file]['STN-ID'] = station_data[names1[count]]['STN-ID']
        all_data[file]['LAT'] = station_data[names1[count]]['LAT']
        all_data[file]['LON'] = station_data[names1[count]]['LON']
        all_data[file]['BEGIN-DATE'] = station_data[names1[count]]['BEGIN-DATE']
        all_data[file]['END-DATE'] = station_data[names1[count]]['END-DATE']
        all_data[file]['ELEVATION'] = station_data[names1[count]]['ELEVATION (Meters)']
        all_data[file]['MATCH'] = names1[count]
        all_data[file]['MATCH-TYPE'] = 'names1'
    elif names2[count] in station_data.keys():
        all_data[file]['STN-ID'] = station_data[names2[count]]['STN-ID']
        all_data[file]['LAT'] = station_data[names2[count]]['LAT']
        all_data[file]['LON'] = station_data[names2[count]]['LON']
        all_data[file]['BEGIN-DATE'] = station_data[names2[count]]['BEGIN-DATE']
        all_data[file]['END-DATE'] = station_data[names2[count]]['END-DATE']
        all_data[file]['ELEVATION'] = station_data[names2[count]]['ELEVATION (Meters)']
        all_data[file]['MATCH'] = names2[count]
        all_data[file]['MATCH-TYPE'] = 'names2'
    elif names3[count] in station_data.keys():
        all_data[file]['STN-ID'] = station_data[names3[count]]['STN-ID']
        all_data[file]['LAT'] = station_data[names3[count]]['LAT']
        all_data[file]['LON'] = station_data[names3[count]]['LON']
        all_data[file]['BEGIN-DATE'] = station_data[names3[count]]['BEGIN-DATE']
        all_data[file]['END-DATE'] = station_data[names3[count]]['END-DATE']
        all_data[file]['ELEVATION'] = station_data[names3[count]]['ELEVATION (Meters)']
        all_data[file]['MATCH'] = names3[count]
        all_data[file]['MATCH-TYPE'] = 'names3'
    elif close_name[0] in station_data.keys():
        all_data[file]['STN-ID'] = station_data[close_name[0]]['STN-ID']
        all_data[file]['LAT'] = station_data[close_name[0]]['LAT']
        all_data[file]['LON'] = station_data[close_name[0]]['LON']
        all_data[file]['BEGIN-DATE'] = station_data[close_name[0]]['BEGIN-DATE']
        all_data[file]['END-DATE'] = station_data[close_name[0]]['END-DATE']
        all_data[file]['ELEVATION'] = station_data[close_name[0]]['ELEVATION (Meters)']
        all_data[file]['MATCH'] = close_name[0]
        all_data[file]['MATCH-TYPE'] = 'close_match'
    else:
        bad.append(file)
    count = count + 1

#%% Export data to csv

fn = ['STN-ID','ST-NAME','LAT','LON','DATE','PRECIP']

with open(r'D:\Windows\Users\tasichcm\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\Daily\daily_precip.csv','wb') as f:
    writer = csv.DictWriter(f,fieldnames=fn)
    writer.writeheader()
    for station in all_data.keys():
        for date in sorted(all_data[station]['PRECIP'].keys()):
            writer.writerow({'STN-ID':all_data[station]['STN-ID'],
            'ST-NAME':all_data[station]['ST-NAME'],
            'LAT':all_data[station]['LAT'],'LON':all_data[station]['LON'],
            'DATE':date,'PRECIP':all_data[station]['PRECIP'][date]})