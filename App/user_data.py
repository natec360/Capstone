# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 20:32:30 2023

@author: Matt Pitz
"""

#libraries
import random
import pandas as pd
from datetime import datetime

def get_user_data():
    while True:  
        user_type = input("Are you a new user? (yes/no): ")
        try:
            user_type.lower() in ['yes', 'no']
            break
        except ValueError:
            print("Please respond with 'yes', or 'no'.")
            
    #User ID
    if user_type.lower() == 'yes':
        user_id = random.randint(10000, 20000)  # Assign a random 6 digit number as user id
        print(f"Your user ID is {user_id}")
        new_user = 1
    else:
        user_id = input("Please enter your user id: ")
        new_user = 0
  
    #ask how many days they ran
    while True:
            num_days = input("How many days did you run in the last 7 days?: ")
            try:
                num_days = int(num_days)  # Check if the number of days is a valid integer
                if 0 <= num_days <= 7:  # The number of days should be between 0 and 7
                    break
                else:
                    print("Invalid number of days. Please enter a number between 0 and 7.")
            except ValueError:
                print("Invalid number of days. Please enter a number.")

                
    #collect gender and age
    while True:
        gender = input("What is your gender? (M/F/Other) ")
        try:
            gender.lower() in ['m', 'f', 'other']
            break
        except ValueError:
            print("Please respond with 'M', 'F', or 'Other'.")
        

    while True:          
        age = input("What is your age? ")
        try:
            age = int(age)
            if age >= 18:
                if 18 <= age <= 34:
                    age_group = "18 - 34"
                elif 35 <= age <= 54:
                    age_group = "35 - 54"
                else:
                    age_group = "55 +"
                break
            else:
                print("Minimum age is 18. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid number for age.")

    #collect information on each run
    data = []
    for _ in range(num_days):
        while True:
            date = input("Enter a date you ran in MM/DD/YYYY format: ")
            try:
                datetime.strptime(date, '%m/%d/%Y')  # Check if the date is valid
                date = datetime.strptime(date, '%m/%d/%Y')
                break
            except ValueError:
                print("Invalid date. Please enter a date in MM/DD/YYYY format.")

        while True:
            num_value = input("How many kilometers did you run?: ")
            try:
                num_value = float(num_value)  # Check if the numeric value is valid
                break
            except ValueError:
                print("Invalid numeric value. Please enter a numeric value.")

        while True:
            time_value = input("What was the total run time in HH:MM:SS format?: ")
            try:
                datetime.strptime(time_value, '%H:%M:%S')  # Check if the time value is valid
                time_value = datetime.strptime(time_value, '%H:%M:%S')
                break
            except ValueError:
                print("Invalid time value. Please enter a time value in HH:MM:SS format.")
        
        data.append([date, num_value, time_value])
    
    df = pd.DataFrame(data, columns=['Date', 'Distance', 'Duration'])
    df['user_id'] = user_id
    #adjust duration format
    df['Duration'] = df['Duration'].apply(lambda x: x.strftime('%H:%M:%S'))
    
    # Extract the month from the first row of the DataFrame
    month = None
    if len(df) > 0:
        month = df.loc[0, 'Date'].month
        
    return new_user, user_id, gender, age_group, month, df


def get_run_plan():
    while True:
        try:
            km_this_week = int(input("How many km do you plan to run this week? "))
            if km_this_week < 0:
                print("Distance cannot be negative. Please try again.")
                continue

            days_to_run = int(input("How many days do you plan to run? "))
            if days_to_run < 0 or days_to_run > 7:
                print("Days to run should be between 0 and 7. Please try again.")
                continue

            medium_intensity_runs = int(input("How many medium intensity runs would you like? "))
            if medium_intensity_runs < 0:
                print("Runs cannot be negative. Please try again.")
                continue

            high_intensity_runs = int(input("How many high intensity runs would you like? "))
            if high_intensity_runs < 0:
                print("Runs cannot be negative. Please try again.")
                continue
            
            sunday_long_run = input("Would you like a Sunday long run? (yes/no) ")
            if sunday_long_run.lower() not in ['yes', 'no']:
                print("Please respond with 'yes' or 'no'.")
                continue

            return km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run == 'yes'
        except ValueError:
            print("Invalid input. Please enter a valid number.")

#eof
