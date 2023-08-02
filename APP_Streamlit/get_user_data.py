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

    # User Type
    user_type = st.radio("Are you a new user?", ('Yes', 'No'))
    #new_user = True if user_type == 'Yes' else False
    new_user = 1 if user_type == 'Yes' else 0

    user_id = None  # Initialize user_id variable to None
    missing_fields = []

    if new_user:
        # New User Info
        st.header("New User Information")
        
        # Generate a random user ID for new users
        user_id = generate_random_user_id()

        '''
        age = st.number_input("What is your age?", min_value=18, step=1) 
        age = int(age)
        if age >= 18:
            if 18 <= age <= 34:
                age_group = "18 - 34"
            elif 35 <= age <= 54:
                age_group = "35 - 54"
            else:
                age_group = "55 +"
        
        gender = st.selectbox("What is your gender?", ('Male', 'Female','Other'))
        distance_last_week = st.number_input("Distance run last week (in kilometers):", min_value=0.0, step=0.1)
        pace_last_week = st.time_input("Average pace last week:", value=datetime.strptime('00:00:00', '%H:%M:%S'))
        num_days_run_last_week = st.slider("Number of days run in last week:", 0, 7)
        days_since_last_run = st.slider("Days since last run:", 0, 30)
        '''

        # Additional data collection for new users can be added here
    else:
        # Returning User Info
        st.header("Returning User Information")
        
        user_id = st.text_input("Please enter your user ID:")

        # Additional data collection for returning users can be added here
        if user_id:
            num_days_run_last_week = st.slider("Number of days run in last week:", 0, 7)
            days_since_last_run = st.slider("Days since last run:", -1, 30)

            # Check for missing fields for returning users
            if not num_days_run_last_week:
                missing_fields.append("Number of days ran in last week")
            if not days_since_last_run:
                missing_fields.append("Days since last run")



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
        pace_hours, pace_minutes, pace_seconds = map(int, pace_last_week_input.split(':'))
        pace_last_week = timedelta(hours=pace_hours, minutes=pace_minutes, seconds=pace_seconds)
    except ValueError:
        pace_last_week = timedelta(seconds=0)  # Set to default value if input is invalid

    # Convert the timedelta object to a string for displaying in the app
    str_pace_last_week = str(pace_last_week)


    num_days_run_last_week = st.slider("Number of days ran last week:", 0, 7)
    days_since_last_run = st.slider("Days since last run:", 0, 30)


    # Information on Each Run

    st.header("Information on Each Run")
    data = []
    for i in range(num_days_run_last_week):
        st.subheader(f"Day {i+1}")
        date = st.date_input("Enter a date you ran:", key=f"date_{i}")
        distance_value = st.number_input("How many kilometers did you run?", min_value=0.0, step=0.1, key=f"distance_{i}")
        pace_value = st.text_input("What was the total run pace?", key=f"pace_{i}", value="00:00")

        try:
            # Convert the input pace to a timedelta object
            pace_minutes, pace_seconds = map(int, pace_value.split(':'))
            pace_timedelta = timedelta(minutes=pace_minutes, seconds=pace_seconds)
        except ValueError:
            # Handle any invalid "Duration" values by setting them to None or any default value you prefer
            pace_timedelta = None  # or timedelta(seconds=0) for default value

        data.append([date, distance_value, pace_timedelta])

    df = pd.DataFrame(data, columns=['Date', 'Distance (in km)', 'Pace'])

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
        return None, None, None, None, None, None, None, None, None

    if new_user:
        return new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, df, user_id
    else:
        return new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, df, user_id
