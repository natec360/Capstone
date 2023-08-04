import streamlit as st
from database_utils import load_data, update_database, database_for_recommender
from recommender import generate_run_ratings, return_run_schedule
from get_user_data import get_user_data, get_run_plan
from welcome_page import show_welcome_page
from main import main



def main():


    # Show welcome page
    show_welcome_page()


    # Load data
    raw_df = load_data()
    filtered_df = None

    # Get run schedule based on user input
    run_schedule = main()

    st.title("Runner Training Plan Recommender")

    # User Input Section
    st.header("User Input Form")
    new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, month, user_id = get_user_data()
    #new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, month, df, user_id = get_user_data()

    # Update user database
    if new_user:
        updated_user_df = None
        st.warning("Please complete the 'Information on Each Run' section below.")
    else:
        updated_user_df = update_database()

    # Prepare data for the recommender system
    if not new_user and updated_user_df is not None:
        filtered_df = database_for_recommender()

    if not new_user or (new_user and updated_user_df is not None):
        # Generate run ratings
        run_recommendations = generate_run_ratings()
        
        # Ask for this week's plan
        if run_recommendations is not None:
            st.subheader("Runner Training Plan - This Week's Plan")
            km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan()

            # Return the optimized run schedule
            if km_this_week and days_to_run and medium_intensity_runs is not None and high_intensity_runs is not None and sunday_long_run is not None:
                number_of_days = days_to_run
                weekly_target = km_this_week
                long_run = 'yes' if sunday_long_run else 'no'
                run_schedule = return_run_schedule()

                # Display the schedule
                st.subheader("Your Run Schedule for This Week:")
                st.dataframe(run_schedule)

    # Display user input data for verification
    st.subheader("User Input Data:")
    if new_user:
        st.write("New User ID:", user_id)
    else:
        st.write("Returning User ID:", user_id)

    st.write("Age Group:", age_group)
    st.write("Gender:", gender)
    st.write("Distance Last Week (in km):", distance_last_week)
    st.write("Average Pace Last Week:", pace_last_week)
    st.write("Number of Days Run Last Week:", num_days_run_last_week)
    st.write("Days Since Last Run:", days_since_last_run)
    st.write("Current Month:", month)

    if updated_user_df is not None:
        st.subheader("Additional User Run Data:")
        st.dataframe(updated_user_df)

    if filtered_df is not None:
        st.subheader("Filtered Data for Recommender System:")
        st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
