# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import json,os
import pandas as pd

#Set display for all columns
pd.set_option('display.max_columns', 100)

#Import methods from processing.py
from processing import Processing

#Ignore warnings for chained assignments
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

p = Processing()


#Create variables to get all files
subfolders = p.data_directory()
dir_list = p.data_files(subfolders)
data_directory = p.datadir+'/'
all_tables = {}

#Run a loop for all available subfolders on Data
for x in subfolders:
    
    dir_list = p.data_files([x])
    df_name = x.replace(data_directory,'')
    initial_data = pd.DataFrame()
    
    #Run a loop on each folder in Data to get all json files
    for i in range(len(dir_list)):
        try:
            with open(dir_list[i]) as json_file:
                #Load json to a variable to be processed
                data = json.load(json_file)
                        
                #Determine whether to insert a create or update data using different methods and combine it with current dataframe
                if data['op'] == 'c':
                    delta_data = p.create(data)
                    initial_data = pd.concat([initial_data, delta_data], ignore_index=True)
                    
                elif data['op'] == 'u':
                    data_id = data['id']
                    delta_data = p.update(initial_data,data_id,data,len(initial_data))
                    initial_data = pd.concat([initial_data, delta_data], ignore_index=True)
                
                
        except Exception as e: 
            #Print error if there is any file that is invalid
            print("There is an invalid file: ",dir_list[i], e)
            continue
                
    #Print each table according to its folder name
    print ('This is the table for: ' + df_name)
    print (initial_data)
    #Dict holding all tables as values with folder name as keys
    all_tables[df_name] = initial_data
 
try:    
    #Join all three tables and print
    join_all_tables = pd.merge(all_tables['accounts'], all_tables['cards'], left_on='card_id',right_on='card_id', how='left')
    join_all_tables = pd.merge(join_all_tables, all_tables['savings_accounts'], left_on='savings_account_id',right_on='savings_account_id', how='left')
    print ("This is the joined three tables")
    print (join_all_tables)
    
    #Join cards and accounts and print
    cards_account = p.merge_asof(all_tables['cards'], all_tables['accounts'],'timestamp','card_id','backward')
    print ("This is the Cards and Accounts joined table")
    print (cards_account)
    
    #Join savings accounts and cards and print
    savings_accounts_account = p.merge_asof(all_tables['savings_accounts'], all_tables['accounts'],'timestamp','savings_account_id','backward')
    print ("This is the Cards and Accounts joined table")
    print (savings_accounts_account)
    
    #Print transaction on cards
    print ("Show all transactions on Cards")
    p.count_cards_trx(cards_account, "credit_used", "monthly_limit", "timestamp", "card_id")
    
    #Print transaction on savings accounts
    print ("Show all transactions on Savings Account")
    p.count_savings_account_trx(savings_accounts_account, "balance", "timestamp", "savings_account_id")
    
    
except Exception as e: 
    print(repr(e))
    


