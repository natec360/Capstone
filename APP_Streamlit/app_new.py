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


    # If any of the required user inputs are missing, display an error message
    if new_user is None:
        st.error("Please fill in all required fields.")
        return

    # Collect the runner training plan for this week using get_run_plan function
   #km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan()
    km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan()


    # If any of the required run plan inputs are missing, display an error message
    if km_this_week is None:
        st.error("Please fill in all required fields.")
        return

  # Call the main() function from main.py
  #  if new_user is not None and user_id is not None and gender is not None and age_group is not None and month is not None and updated_user_df is not None and weekly_target is not None and days_to_run is not None and medium_intensity_runs is not None and high_intensity_runs is not None and long_run is not None:
   #     run_schedule = generate_run_schedule_for_user(new_user, user_id, gender, age_group, month, updated_user_df, weekly_target, days_to_run, medium_intensity_runs, high_intensity_runs, long_run)

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
