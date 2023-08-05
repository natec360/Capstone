import streamlit as st
import random
from datetime import datetime, timedelta
import pandas as pd


def generate_random_user_id():
    """Generate a random user ID."""
    return f"{random.randint(10000, 99999)}"

def parse_pace_string(pace_str):
    try:
        pace_parts = pace_str.split(":")
        if len(pace_parts) == 3:  # Format is "00:21:14" (HH:MM:SS)
            hours = int(pace_parts[0])
            minutes = int(pace_parts[1])
            seconds = int(pace_parts[2])
        else:  # Format is "21:14" (MM:SS)
            hours = 0
            minutes = int(pace_parts[0])
            seconds = int(pace_parts[1])
        pace_timedelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return pace_timedelta
    except:
        return None


def format_pace_string(pace_timedelta):
    if pace_timedelta:
        hours, remainder = divmod(pace_timedelta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return "00:00:00"


def get_user_data():
    st.title("Runner Training Plan - User Input Form")
    global new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, month, user_id
    #new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, month, user_id
   
    # User Type
    new_user_input = st.radio("Are you a new user?", ('Yes', 'No'), key="user_type")  # Add key to the radio widget
    new_user = 1 if new_user_input == 'Yes' else 0

    user_id = None  # Initialize user_id variable to None
    missing_fields = []

    if new_user:
        # New User Info
        st.header("New User Information")
        
        # Generate a random user ID for new users
        user_id = generate_random_user_id()


    else:
        # Returning User Info
        st.header("Returning User Information")
        
        user_id = st.text_input("Please enter your user ID:")
        '''
        # Additional data collection for returning users can be added here
        if user_id:
            num_days_run_last_week = st.slider("Number of days run in last week:", 0, 7)
            days_since_last_run = st.slider("Days since last run:", -1, 30)

            # Check for missing fields for returning users
            if not num_days_run_last_week:
                missing_fields.append("Number of days ran in last week")
            if not days_since_last_run:
                missing_fields.append("Days since last run")
        '''


    # Age Group
    age = st.number_input("What is your age?", min_value=18, step=1)
    age = int(age)
    if age >= 18:
        if 18 <= age <= 34:
            age_group = "18 - 34"
        elif 35 <= age <= 54:
            age_group = "35 - 54"
        else:
            age_group = "55 +"

    gender = st.selectbox("What is your gender?", ('Male', 'Female', 'Other'))
    distance_last_week = st.number_input("Distance ran last week (in kilometers):", min_value=0.0, step=0.1)
    pace_last_week_input = st.text_input("Average pace last week in HH:MM:SS:", value='00:00:00')

    try:
        # Convert the input pace to a timedelta object
        #pace_hours, pace_minutes, pace_seconds = map(int, pace_last_week_input.split(':'))
        #pace_last_week = datetime.strptime(pace_value, '%H:%M:%S')
        pace_last_week = datetime.strptime(pace_last_week_input, '%H:%M:%S')
    except ValueError:
        pace_last_week = None  # Set to default value if input is invalid

    # Convert the timedelta object to a string for displaying in the app
    str_pace_last_week = str(pace_last_week.strftime("%H:%M:%S"))


    num_days_run_last_week = st.slider("Number of days ran last week:", 0, 7)
    days_since_last_run = st.slider("Days since last run:", 0, 30)


    # Information on Each Run

    st.header("Information on Each Run")
    data = []
    for i in range(num_days_run_last_week):
        st.subheader(f"Day {i+1}")
        date = st.date_input("Enter a date you ran:", key=f"date_{i}")
        distance_value = st.number_input("How many kilometers did you run?", min_value=0.0, step=0.1, key=f"distance_{i}")
        pace_value = st.text_input("What was the total run time?", key=f"pace_{i}", value="00:00:00")

        try:
            # Convert the input pace to a timedelta object
            #pace_minutes, pace_seconds = map(int, pace_value.split(':'))
            pace_timedelta = datetime.strptime(pace_value, '%H:%M:%S')
        except ValueError:
            # Handle any invalid "Duration" values by setting them to None or any default value you prefer
            pace_timedelta = None  # or timedelta(seconds=0) for default value

        data.append([date, distance_value, pace_timedelta])

    df = pd.DataFrame(data, columns=['Date', 'Distance', 'Duration'])
    
    # Extract the month from the first row of the DataFrame
    month = None
    if len(df) > 0:
        month = df.loc[0, 'Date'].month

    # Validate inputs
    error_msg = ""
    if new_user:
        if not age or not gender or not distance_last_week or not pace_last_week or not num_days_run_last_week or not days_since_last_run:
            error_msg += "Please fill in all new user information fields.\n"
    else:
        if not user_id:
            error_msg += "Please enter your user ID for returning users.\n"

    if missing_fields:
        error_msg += f"Please fill in the following fields for returning users: {', '.join(missing_fields)}.\n"

    if error_msg:
        st.error("Errors found:\n" + error_msg)
        return None, None, None, None, None, None, None, None, None, None

    if new_user:
        return new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, month, df, user_id
    else:
        return new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, month, df, user_id



def get_run_plan():
    st.header("Runner Training Plan - This Week's Plan")

    km_this_week = st.number_input("How many km do you plan to run this week?", min_value=0, step=1, key="km_this_week")
    days_to_run = st.slider("How many days do you plan to run?", 0, 7, key="days_to_run")
    medium_intensity_runs = st.number_input("How many medium intensity runs would you like?", min_value=0, step=1, key="medium_intensity_runs")
    high_intensity_runs = st.number_input("How many high intensity runs would you like?", min_value=0, step=1, key="high_intensity_runs")
    sunday_long_run = st.radio("Would you like a Sunday long run?", ('Yes', 'No'), key="sunday_long_run_radio")
    
    # Validate inputs
    error_msg = ""
    if km_this_week is None or days_to_run is None or medium_intensity_runs is None or high_intensity_runs is None or sunday_long_run is None:
        error_msg = "Please enter all information in fields."

    if error_msg:
        st.error(error_msg)
        # Return None to indicate an error
        return None, None, None, None, None
    
    # Set high_intensity_runs to 0 if it is not provided by the user
    if high_intensity_runs is None:
        high_intensity_runs = 0
    
    # Set high_intensity_runs to 0 if it is not provided by the user
    if medium_intensity_runs is None:
        medium_intensity_runs = 0

    return km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run == 'Yes'