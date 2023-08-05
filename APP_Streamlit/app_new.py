import streamlit as st
from database_utils import load_data, update_database, database_for_recommender
from recommender import generate_run_ratings, return_run_schedule
from get_user_data import get_user_data, get_run_plan
from welcome_page import show_welcome_page
from main import main

def main_app():
    
    show_welcome_page()

    # Collect user information using get_user_data function
    new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, month, new_user_df, user_id = get_user_data()

    if new_user is not None:
        # Get the training plan for the user
        km_this_week, number_of_days, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan()

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
    st.table(new_user_df)

    # Collect the runner training plan for this week using get_run_plan function
    #km_this_week, number_of_days, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan()

    
    st.subheader("Run Plan Data")
    run_plan_data = {
        "User ID": user_id,
        "Age Group": age_group,
        "Km this week": km_this_week,
        "Days to run": number_of_days,
        "Medium intensity runs": medium_intensity_runs,
        "High intensity runs": high_intensity_runs,
        "Sunday long run": "Yes" if sunday_long_run else "No"
    }
    st.table(run_plan_data)


    # If any of the required run plan inputs are missing, display an error message
    if km_this_week is None:
        st.error("Please fill in all required fields.")
        return

    #load in recommender dataset
    raw_df = load_data()
    
    #st.table(raw_df['current_month'].sample(10))

     # Call the main function to generate the run schedule based on user inputs
    if st.button("Generate Run Plan"):    
    
        #create db for retrainging recommender
        st.write(f"Age Group: {age_group}")
        filtered_df = database_for_recommender(raw_df, new_user_df, gender, age_group, month, number_of_days, km_this_week)

        #Create recommender df
        recommendations_df = generate_run_ratings(filtered_df,user_id, km_this_week, number_of_days)
    
        run_schedule = return_run_schedule(recommendations_df, number_of_days, km_this_week, medium_intensity_runs, high_intensity_runs, sunday_long_run)

        # Display the generated run schedule to the user
        if run_schedule is not None:
            st.header("Generated Run Schedule")
            st.table(run_schedule)
        else:
            st.write("Error: Unable to generate the run schedule.")

if __name__ == "__main__":
    main_app()
