import streamlit as st
import pandas as pd
from welcome_page import show_welcome_page
from get_user_data import get_user_data
from run_plan_page import get_run_plan
from database_utils import update_database, database_for_recommender
from recommender import generate_run_ratings, return_run_schedule

# Set the Streamlit page configuration
st.set_page_config(page_title="Runner Training Plan App", page_icon="🏃‍♂️")

# Create a sidebar navigation menu
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Welcome", "User Input", "Run Plan", "Table Input Results"])  # Add the new page

# Initialize the show_run_plan_page session state variable to False
if "show_run_plan_page" not in st.session_state:
    st.session_state.show_run_plan_page = False

# Create a state variable to track the current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "Welcome"

# Create a state variable to track the reset action
if "reset" not in st.session_state:
    st.session_state.reset = False

# Global variables
new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, new_user_df, user_id = None, None, None, None, None, None, None, None, None
km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run = None, None, None, None, None
user_db_data = pd.DataFrame()

# Format the timedelta as HH:MM:SS
def format_pace_string(pace_timedelta):
    if pace_timedelta:
        hours, remainder = divmod(pace_timedelta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return "00:00:00"

# Main function to run the Streamlit app
def main():
    global new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, new_user_df, user_id
    global km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run, user_db_data

    # Call the corresponding function based on the current page
    if st.session_state.current_page == "Welcome":
        show_welcome_page()
        # Add a "Start" button on the welcome page with a unique key
        if st.button("Click here to begin", key="start_button"):
            # Set the current page to "User Input" when the button is clicked
            st.session_state.current_page = "User Input"
    
    elif st.session_state.current_page == "User Input":
        handle_user_input()
    
    elif st.session_state.current_page == "Run Plan":
        generate_run_plan()

    elif st.session_state.current_page == "Table Input Results":
        show_table_input_results()

    # Add a "Reset" button to the sidebar
    if st.sidebar.button("Reset"):
        st.session_state.reset = True
        st.experimental_rerun()

def handle_user_input():
    global new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, new_user_df, user_id

    # Check if reset button is clicked
    if st.session_state.reset:
        # Clear user input data
        st.session_state.clear()
        st.session_state.reset = False
        st.session_state.current_page = "Welcome"
        st.experimental_rerun()

    new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, new_user_df, user_id = get_user_data()
    
    if new_user_df is not None:
        # Display user data
        st.write("User Data")
        st.write(f"New User: {'Yes' if new_user else 'No'}")
        st.write(f"User ID: {user_id}")
        st.write(f"Age Group: {age_group}")
        st.write(f"Gender: {gender}")
        st.write(f"Distance Ran Last Week (in km): {distance_last_week}")
        st.write(f"Average Pace Last Week: {format_pace_string(pace_last_week)}")
        st.write(f"Number of Days Ran Last Week: {num_days_run_last_week}")
        st.write(f"Days Since Last Run: {days_since_last_run}")
        
        st.write("Run Data:")
        st.write(new_user_df)

        if new_user:
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

    # Show user data in a table format
    if new_user is not None:
        st.write("User Data Summary:")
        user_data_summary = pd.DataFrame({
            "Field": ["User ID", "Age Group", "Gender", "Distance Run Last Week (in km)", "Average Pace Last Week", "Number of Days Run in Last Week", "Days Since Last Run"],
            "Value": [user_id, age_group, gender, distance_last_week, format_pace_string(pace_last_week), num_days_run_last_week, days_since_last_run]
        })
        st.dataframe(user_data_summary)

        # Check if any field is missing for returning users
        if not new_user:
            missing_fields = []
            if None in [num_days_run_last_week, days_since_last_run]:
                if num_days_run_last_week is None:
                    missing_fields.append("Number of Days Ran in Last Week")
                if days_since_last_run is None:
                    missing_fields.append("Days Since Last Run")
                st.error("Please fill in the following fields for returning users: " + ", ".join(missing_fields) + ".")

def generate_run_plan():
    global km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run, user_db_data

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
        # Assume you have a variable named 'month' that contains the current month number (e.g., 8 for August)
        user_db_data = update_database(new_user, gender, age_group, month, km_this_week, days_to_run, user_id, new_user_df)
        filtered_data = database_for_recommender(user_db_data, new_user_df, gender, age_group, month, days_to_run, km_this_week)
        st.write("Updated user database and retrieved recommendations.")
        st.write("Recommendations:")
        st.write(filtered_data)

        # Generate run ratings and return the schedule
        run_recommendations = generate_run_ratings(filtered_data, user_id, km_this_week, days_to_run)
        run_schedule = return_run_schedule(run_recommendations, days_to_run, km_this_week, medium_intensity_runs, high_intensity_runs, sunday_long_run)

def show_table_input_results():
    st.title("Table Input Results")
    if new_user_df is not None:
        st.subheader("User Input Data")
        st.write(new_user_df)

    if km_this_week is not None and days_to_run is not None:
        st.subheader("Run Plan Data")
        run_plan_data = {
            "Km this week": [km_this_week],
            "Days to run": [days_to_run],
            "Medium intensity runs": [medium_intensity_runs],
            "High intensity runs": [high_intensity_runs],
            "Sunday long run": ['Yes' if sunday_long_run else 'No']
        }
        st.write(pd.DataFrame(run_plan_data))

if __name__ == "__main__":
    main()
