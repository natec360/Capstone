import streamlit as st
import random
from datetime import datetime
import pandas as pd

def get_run_plan():
    st.title("Runner Training Plan - This Week's Plan")

    km_this_week = st.number_input("How many km do you plan to run this week?", min_value=0, step=1)
    days_to_run = st.slider("How many days do you plan to run?", 0, 7)
    medium_intensity_runs = st.number_input("How many medium intensity runs would you like?", min_value=0, step=1)
    high_intensity_runs = st.number_input("How many high intensity runs would you like?", min_value=0, step=1)
    sunday_long_run = st.radio("Would you like a Sunday long run?", ('Yes', 'No'))

    # Validate inputs
    error_msg = ""
    if not km_this_week or not days_to_run or not medium_intensity_runs or not high_intensity_runs or not sunday_long_run:
        error_msg = "Please enter all information in fields."

    if error_msg:
        st.error(error_msg)
        # Return None to indicate an error
        return None, None, None, None, None

    return km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run == 'Yes'