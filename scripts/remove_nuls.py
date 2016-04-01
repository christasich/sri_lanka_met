# -*- coding: utf-8 -*-
"""
Created on Wed Feb 04 13:01:01 2015

@author: Christopher M. Tasich
@organization: Vanderbilt University
"""
#%% Import packages

import os,shutil,csv
import ctlib as cl

#%% Import data

dir = r'D:\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\Daily\Precip'
files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
str = '\x00'

#%% Create output directory

wdir = r'D:\Dropbox (ISEE Bangladesh)\Programming\Python\Projects\Gunda\Data\Daily\Precip\new'
if os.path.exists(wdir):
    shutil.rmtree(wdir)
os.makedirs(wdir)

#%% Initialize variables

nulfiles = []

#%% Scan files for NUL bytes

for file in files:
    if cl.strscan(file,dir,str):
        nulfiles.append(file)

#%% Make copy of file with NUL bytes and reaplace NULs with blanks

for file in nulfiles:
    cl.repstring(file,dir,wdir,str,'')

#%%# Copy modified files to original directory then delete working directory

for file in nulfiles:
    shutil.copy(os.path.join(wdir,file),dir)
shutil.rmtree(wdir)