import random
import pandas as pd
from datetime import datetime

def get_user_data():
    user_type = input("Are you a new user? (yes/no): ")
    
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


    #collect information on each run
    data = []
    for _ in range(num_days):
        while True:
            date = input("Enter a date you ran in MM/DD/YYYY format: ")
            try:
                datetime.strptime(date, '%m/%d/%Y')  # Check if the date is valid
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
                break
            except ValueError:
                print("Invalid time value. Please enter a time value in HH:MM:SS format.")
        
        data.append([date, num_value, time_value])
    
    df = pd.DataFrame(data, columns=['Date', 'Numeric Value', 'Time Value'])
    return new_user, user_id, df

#eof
