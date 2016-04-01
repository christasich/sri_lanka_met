# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 15:05:54 2015

@author: Christopher M. Tasich
@organization: Vanderbilt University
"""
#%% Import packages

import csv,os,re
import difflib as dl

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
                precip[row['Date']] = row['None']
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
                precip[row['Date']] = row['Precip']
        precip_data['PRECIP'] = precip
        all_data[file] = precip_data
        
#%% Export data to csv

fn = ['ST-NAME','LAT','LON','DATE','PRECIP']

with open(r'D:\Windows\Users\tasichcm\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\Daily\out.csv','wb') as f:
    writer = csv.DictWriter(f,fieldnames=fn)
    writer.writeheader()
    for station in all_data.keys():
        for date in sorted(all_data[station]['PRECIP'].keys()):
            writer.writerow({'ST-NAME':all_data[station]['ST-NAME'],
                           'LAT':all_data[station]['LAT'],
                           'LON':all_data[station]['LON'],'DATE':date,
                           'PRECIP':all_data[station]['PRECIP'][date]})

#%% Compare precip stations to station list

names=[]
alt_names=[]
count=0
good=[]
bad=[]

for file in files:
    names.append(file[:-17].upper())
    if r'(' in names[count]:
        alt_names.append(re.findall(r'\(([^\)]+)\)',names[count])[0] + ' ESTATE')
    else:
        alt_names.append(names[count])
    if names[count] or alt_names[count] in station_data.keys():
        good.append(names[count])
    elif dl.get_close_matches(names[count],station_data.keys()):
        good.append(names[count])
    elif dl.get_close_matches(alt_names[count],station_data.keys()):
        good.append(names[count])
    else:
        bad.append(names[count])
    count = count + 1
    
if len(names) == len(good):
    print "It's all good!"