import streamlit as st
import pandas as pd
from datetime import datetime
from get_user_data import get_user_data
from run_plan_page import get_run_plan

# Set the Streamlit page configuration
st.set_page_config(page_title="Runner Training Plan App", page_icon="🏃‍♂️")

# Create a sidebar navigation menu
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["User Input", "Run Plan"])

# Initialize the show_run_plan_page session state variable to False
if "show_run_plan_page" not in st.session_state:
    st.session_state.show_run_plan_page = False

if page == "User Input":
    user_data = get_user_data()

    if user_data is not None:
        new_user, *user_info, df, user_id = user_data

        if new_user:
            # Display new user data
            st.write("New User Data:")
            st.write(f"Age: {user_info[0]}")
            st.write(f"Gender: {user_info[1]}")
            st.write(f"Distance Run Last Week (in km): {user_info[2]}")
            st.write(f"Average Pace Last Week: {user_info[3].strftime('%H:%M:%S')}")
            st.write(f"Number of Days Run in Last Week: {user_info[4]}")
            st.write(f"Days Since Last Run: {user_info[5]}")
            st.write("Run Data:")
            st.write(df)

            # Validate inputs for new users
            if None in user_info:
                st.error("Please fill in all new user information fields.")
            else:
                # Add a "Next" button for new users
                if st.button("Next"):
                    # Set show_run_plan_page to True when the button is clicked
                    st.session_state.show_run_plan_page = True
                    # Trigger a rerun of the script to automatically switch to the "Run Plan" page
                    st.experimental_rerun()
        else:
            # Display returning user data
            st.write("Returning User Data:")
            st.write(f"User ID: {user_id}")
            st.write(f"Number of Days Run in Last Week: {user_info[0]}")
            st.write(f"Days Since Last Run: {user_info[1]}")
            st.write("Run Data:")
            st.write(df)

            # Validate inputs for returning users
            if None in user_info:
                st.warning("Please enter all required information for returning users.")
            else:
                # Check if all required information is present for returning users
                if user_id is not None and user_info[0] is not None and user_info[1] is not None:
                    # Add a "Next" button for returning users
                    if st.button("Next"):
                        # Set show_run_plan_page to True when the button is clicked
                        st.session_state.show_run_plan_page = True
                        # Trigger a rerun of the script to automatically switch to the "Run Plan" page
                        st.experimental_rerun()

if page == "Run Plan" and st.session_state.show_run_plan_page:
    st.title("Runner Training Plan - Run Input Form")
    km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan()

    # Display the run input data
    st.write("Run Input Data:")
    st.write(f"Km this week: {km_this_week}")
    st.write(f"Days to run: {days_to_run}")
    st.write(f"Medium intensity runs: {medium_intensity_runs}")
    st.write(f"High intensity runs: {high_intensity_runs}")
    st.write(f"Sunday long run: {'Yes' if sunday_long_run else 'No'}")
