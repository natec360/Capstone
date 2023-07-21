# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 20:32:30 2023

@author: Matt Pitz
"""

#libraries
import numpy as np
import pandas as pd
from datetime import datetime

def load_data():
    '''function to load in datasets to memory'''
    
    
    #load in csv data
    raw_df_2020 = pd.read_csv('../../raw/input_runners_2020.csv')
    raw_df_2019 = pd.read_csv('../../raw/input_runners_2019.csv')

    raw_df = pd.concat([raw_df_2020,raw_df_2019])
    
    #convert months to number
    def mtn(x):
        months = {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr':4,
             'may':5,
             'jun':6,
             'jul':7,
             'aug':8,
             'sep':9,
             'oct':10,
             'nov':11,
             'dec':12
            }
        a = x.strip()[:3].lower()
        try:
            ez = months[a]
            return ez
        except:
            raise ValueError('Not a month')

    raw_df["current_month"] =  raw_df["current_month"].apply(lambda x:mtn(x)) 

    #create user ID
    raw_df["user_id"] = raw_df["athlete"].astype(str) + "." + raw_df["current_month"].astype(str)

    #remove any missings from the data
    raw_df= raw_df[raw_df["prev_month_weekly_km"].notna()]

    #remove 0s
    raw_df = raw_df[raw_df["prev_month_weekly_km"]!=0]
    
    return raw_df
    

def update_database(new_user, gender, age_bucket, month, weekly_target, number_of_days, user_id):
    
    #filter dataset based on targets
    #new_user = new_user
    new_user = 1
    gender = gender
    weekly_target = weekly_target
    age_bucket = age_bucket
    month = month
    number_of_days = number_of_days
    #user_id = user_id
    user_id = '000.0'
    
    #cold start for new user. Assumes long run 2x distance other runs.
    new_user_data = { 
        'user_id' : [user_id] * 2,
        'run_distance_rounded' : [round(weekly_target/6), round(weekly_target/3)],
        'weekly_frequency' : [number_of_days -1, 1]
                    }
    new_user_df = pd.DataFrame(new_user_data)
    return new_user_df
    
    
def database_for_recommender(raw_df, new_user_df, gender, age_bucket, month, number_of_days, weekly_target):
    '''Filter raw data and add user data for recommender system'''
    
    #define objects for Surprise. Must be in user, item, rating order
    filtered_df = raw_df.loc[
        (raw_df['gender'] == gender) &
        (raw_df['age_bucket'] == age_bucket) &
        (raw_df['current_month'] == month) &
        (raw_df['prev_month_weekly_days_run'] > (number_of_days-1)) & 
        (raw_df['prev_month_weekly_days_run'] < (number_of_days+1)) &
        (raw_df['prev_month_weekly_km'] > weekly_target-5) &
        (raw_df['prev_month_weekly_km'] < weekly_target+5)
    ]

    if filtered_df.size <= 15:
        print("insufficient data for",gender,age_bucket,target_kms)
        BREAK 
    
    #append new user data
    filtered_df = pd.concat([filtered_df,new_user_df])
    return filtered_df
    
#EOF