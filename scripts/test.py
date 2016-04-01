# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 14:46:54 2015

@author: tasichcm
"""
import os,csv

dir = r'D:\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\Daily\Precip'
file = r'Delta Estate, East Div  daily precip.dat'
#file = r'Dambatenne daily precip.dat'

fn = ['ST-NAME','LAT','LON','ELEVATION','PRECIP','UNIT']
all_data={}
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
        print header
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