import streamlit as st
import pandas as pd
from welcome_page import show_welcome_page
from get_user_data import get_user_data
from run_plan_page import get_run_plan
from database_utils import update_database, database_for_recommender
from recommender import generate_run_ratings, return_run_schedule

#from main import main  # Import the main function from main.py that will print the run_schedule

#initialize objects
new_user, gender, age_group, month, km_this_week, days_to_run, user_id = None, None, None, None, None, None, None
days_to_run, km_this_week = None, None
medium_intensity_runs, high_intensity_runs, sunday_long_run = None, None, None
new_user_df = pd.DataFrame()
user_db_data = pd.DataFrame()

# Set the Streamlit page configuration
st.set_page_config(page_title="Runner Training Plan App", page_icon="🏃‍♂️")

# Create a sidebar navigation menu
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Welcome", "User Input", "Run Plan"])

# Initialize the show_run_plan_page session state variable to False
if "show_run_plan_page" not in st.session_state:
    st.session_state.show_run_plan_page = False

# Create a state variable to track the current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "Welcome"

# Create a state variable to track the reset action
if "reset" not in st.session_state:
    st.session_state.reset = False

# Handle page transitions
if st.session_state.current_page == "Welcome":
    show_welcome_page()

    # Add a "Start" button on the welcome page with a unique key
    if st.button("Click here to begin", key="start_button"):
        # Set the current page to "User Input" when the button is clicked
        st.session_state.current_page = "User Input"

elif st.session_state.current_page == "User Input":
    # Check if reset button is clicked
    if st.session_state.reset:
        # Clear user input data
        st.session_state.clear()
        st.session_state.reset = False
        st.session_state.current_page = "Welcome"
        st.experimental_rerun()

    new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, new_user_df, user_id = get_user_data()
    
    if new_user_df is not None:
        #new_user, *user_info, df, user_id = user_data

        if new_user:
            # Display new user data
            st.write("New User Data")
            st.write(f"Age: {age_group}")
            st.write(f"Gender: {gender}")
            st.write(f"Distance Run Last Week (in km): {distance_last_week}")
            st.write(f"Average Pace Last Week: {pace_last_week.strftime('%H:%M:%S')}")
            st.write(f"Number of Days Run in Last Week: {num_days_run_last_week}")
            st.write(f"Days Since Last Run: {days_since_last_run}")
            st.write("Run Data:")
            st.write(new_user_df)

            # Validate inputs for new users
            if None in [age_group, gender, distance_last_week, pace_last_week]:
                st.error("Please fill in all new user information fields.")
            else:
                # Add a "Next" button for new users
                if st.button("Next (New User)", key="next_new_user"):
                    # Set show_run_plan_page to True when the button is clicked
                    st.session_state.show_run_plan_page = True
                    # Set the current page to "Run Plan" when the button is clicked
                    st.session_state.current_page = "Run Plan"

        else:
            # Add a "Please Proceed Here" button for returning users if all fields are entered
            if st.button("Please Proceed Here"):
                # Set show_run_plan_page to True when the button is clicked
                st.session_state.show_run_plan_page = True
                # Set the current page to "Run Plan" when the button is clicked
                st.session_state.current_page = "Run Plan"

elif st.session_state.current_page == "Run Plan" and st.session_state.show_run_plan_page:
    # Check if reset button is clicked
    if st.session_state.reset:
        # Clear user input data
        st.session_state.clear()
        st.session_state.reset = False
        st.session_state.current_page = "Welcome"
        st.experimental_rerun()

    st.title("Runner Training Plan - Run Input Form")
    km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan()

    # Display the run input data
    st.write("Run Input Data:")
    st.write(f"Km this week: {km_this_week}")
    st.write(f"Days to run: {days_to_run}")
    st.write(f"Medium intensity runs: {medium_intensity_runs}")
    st.write(f"High intensity runs: {high_intensity_runs}")
    st.write(f"Sunday long run: {'Yes' if sunday_long_run else 'No'}")

    # Update the user database and get the recommendations
    if st.button("Update User Data"):
        
        user_db_data = update_database(new_user, gender, age_group, 7, km_this_week, days_to_run, user_id, new_user_df)
        filtered_data = database_for_recommender(user_db_data, new_user_df, gender, age_group, 7, days_to_run, km_this_week)
        st.write("Updated user database and retrieved recommendations.")
        st.write("Recommendations:")
        st.write(filtered_data)

        # Generate run ratings and return the schedule
        run_recommendations = generate_run_ratings(filtered_data, user_id, km_this_week, days_to_run)
        run_schedule = return_run_schedule(run_recommendations, days_to_run, km_this_week, medium_intensity_runs, high_intensity_runs, sunday_long_run)


'''
    # Call the main function from main.py to get the run schedule
    run_schedule = main()
    st.write("Run Schedule:")
    st.write(run_schedule)
'''

# Add a "Reset" button to the sidebar
if st.sidebar.button("Reset"):
    st.session_state.reset = True
    st.experimental_rerun()
