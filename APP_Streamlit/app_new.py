import streamlit as st
from database_utils import load_data, update_database, database_for_recommender
from recommender import generate_run_ratings, return_run_schedule
from get_user_data import get_user_data, get_run_plan
from welcome_page import show_welcome_page
from main import main

def main_app():
    show_welcome_page()

    # Collect user information using get_user_data function
    new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, month, df, user_id = get_user_data()

    if new_user is not None:
        # Get the training plan for the user
        km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan(num_days_run_last_week)

    else:
        st.error("Please fill in all required fields.")
        return

    # Display user data in a table
    st.subheader("User Data")
    user_data = {
        "New User": "Yes" if new_user else "No",
        "User ID": user_id,
        "Age Group": age_group,
        "Gender": gender,
        "Distance Ran Last Week (in km)": distance_last_week,
        "Average Pace Last Week": pace_last_week,
        "Number of Days Ran Last Week": num_days_run_last_week,
        "Days Since Last Run": days_since_last_run
    }
    st.table(user_data)

    # Display the "Information on Each Run" in a table format
    st.subheader("Information on Each Run (Summary)")
    st.table(df)

    # Collect the runner training plan for this week using get_run_plan function
    #km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan()

    
    st.subheader("Run Plan Data")
    run_plan_data = {
        "User ID": user_id,
        "Km this week": km_this_week,
        "Days to run": days_to_run,
        "Medium intensity runs": medium_intensity_runs,
        "High intensity runs": high_intensity_runs,
        "Sunday long run": "Yes" if sunday_long_run else "No"
    }
    st.table(run_plan_data)


    # If any of the required run plan inputs are missing, display an error message
    if km_this_week is None:
        st.error("Please fill in all required fields.")
        return

     # Call the main function to generate the run schedule based on user inputs
    if st.button("Generate Run"):
        run_schedule = main(new_user, user_id, gender, age_group, month, df, km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run)

        # Display the generated run schedule to the user
        if run_schedule is not None:
            st.header("Generated Run Schedule")
            st.table(run_schedule)
        else:
            st.write("Error: Unable to generate the run schedule.")

if __name__ == "__main__":
    main_app()
