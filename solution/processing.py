#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 21:10:27 2022

@author: reihan
"""

import pandas as pd
import json
import os
import datetime

class Processing():
    
    #Initialize paths and directories
    def __init__(self):
        
        self.workdir = os.getcwd()
        self.parentdir = os.path.dirname(self.workdir)
        self.datadir = self.workdir+'/data'
    
    #Get list of directories on a directory
    def data_directory(self):
        data_list = [ f.path for f in os.scandir(self.datadir) if f.is_dir() ]
        return data_list
    
    #Get list of files on a directory
    def data_files(self,data_list):
        file_list = []
        for d in data_list:
            for path, subdirs, files in os.walk(d):
                for name in files:
                    file_list.append(os.path.join(path,name))
        file_list.sort()
        return file_list
    
    #Get timestamp from UNIX
    def unix_to_ts(self,unix):
        ts = datetime.datetime.fromtimestamp(unix/1000)
        return ts
    
    #Get event key and values as a row
    def get_event(self,event_data,data_row):
        ID = event_data['id']
        data_row['id'] = ID
        op = event_data['op']
        data_row['op'] = op
        ts = event_data['ts']
        data_row['ts'] = ts
        timestamp = self.unix_to_ts(ts)
        data_row['timestamp'] = timestamp
        return data_row
    
    #Get data for create/insert
    def create(self,event_data):
        data_row = event_data['data']
        data_row = self.get_event(event_data, data_row)
        df = pd.DataFrame([data_row])
        return df
    
    #Get data for update on a row
    def update(self,event_data,ID,delta_data,i):
        updated_data = event_data.loc[(event_data['id'] == ID) & (event_data.index == i-1)]
        updated_data = self.get_event(delta_data, updated_data)
        updates = delta_data['set']
        for k,v in updates.items():
            updated_data[k] = v
        return updated_data
    
    def merge_asof(self,data_left,data_right,on,by,direction):
        df = pd.merge_asof(data_left, data_right, 
            on=on, 
            by=by, 
            direction=direction)
        return df


    #Get transactions on savings account
    def count_savings_account_trx(self,data,column,timestamp,iid):
        trx = 0
        temp = 0
        counter = 0
        for i in range(len(data[column])):
            trx = data[column][i] - temp
            temp = data[column][i]
            if trx != 0:
                print ("Transaction amount: {} on {} for ID: ".format(str(trx), str(data[timestamp][i])), data[iid][i])
                counter = counter + 1
        print ("There are a total of {} transactions".format(counter))
        return "All transactions has been shown."
        
    #Get transactions on cards
    def count_cards_trx(self,data,column,limit,timestamp,iid):
        temp = 0
        counter = 0
        for i in range(len(data[column])):
            if data[limit][i] != temp:
                temp = data[limit][i]
                total = 0
            trx = data[column][i] - total
            total = data[column][i] + total
            if trx > 0:
                print ("Transaction amount: {} on {} for ID:".format(str(trx), str(data[timestamp][i])), data[iid][i])
                counter = counter + 1
        print ("There are a total of {} transactions".format(counter))
        return "All transactions has been shown."

        
    
   

