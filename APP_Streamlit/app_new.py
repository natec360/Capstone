import streamlit as st
from database_utils import load_data, update_database, database_for_recommender
from recommender import generate_run_ratings, return_run_schedule
from get_user_data import get_user_data, get_run_plan
from welcome_page import show_welcome_page
from main import main
import time  



def main_page():
     # Use st.session_state to create a session state variable to track the current page
    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    if st.session_state.page == "welcome":
        show_welcome_page()

        # Create an interactive button to move to the main app page
        if st.button("Get Started", key="welcome_button"):  # Provide a unique key for the button
            st.session_state.page = "main_app"
            st.experimental_rerun()  # Rerun the app to move to the main app page

    elif st.session_state.page == "main_app":
        main_app()

def main_app():
    
    # Collect user information using get_user_data function
    new_user, age_group, gender, distance_last_week, pace_last_week, num_days_run_last_week, days_since_last_run, month, new_user_df, user_id = get_user_data()

    if new_user is not None:
        # Get the training plan for the user
        km_this_week, number_of_days, medium_intensity_runs, high_intensity_runs, sunday_long_run = get_run_plan()

    else:
        st.error("Please fill in all required fields to continue.")
        return

     
    # If any of the required run plan inputs are missing, display an error message
    if km_this_week is None:
        st.error("Please fill in all required fields to continue.")
        return

    #injury warning
    if km_this_week >= distance_last_week * 1.2: 
        st.error("Target distance for this week may cause injury. Suggest reducing target")
        return
    
    # Display a progress bar while loading the big data file
    progress_bar = st.progress(0)
    raw_df = None
    loading_complete = False

    with st.spinner("Loading big data file..."):
        # Replace the following loop with your actual data loading process
        for i in range(100):
            progress_bar.progress(i + 1)

        # function call to load your big data file
        raw_df = load_data()

        loading_complete = True

    if loading_complete:
        st.success("Loading complete! Continue to generate plan")


     # Call the main function to generate the run schedule based on user inputs
    if st.button("Generate Run Plan"):    
    
        #create db for retrainging recommender
        st.write(f"Age Group: {age_group}")
        #filtered_df = database_for_recommender(raw_df, new_user_df, gender, age_group, month, number_of_days, km_this_week)
        
        try:
            filtered_df = database_for_recommender(raw_df, new_user_df, gender, age_group, month, number_of_days, km_this_week)
        except Exception as e:
            st.error(f"Error: {e}")
            return

        #Create recommender df
        recommendations_df = generate_run_ratings(filtered_df,user_id, km_this_week, number_of_days)
    
        run_schedule = return_run_schedule(recommendations_df, number_of_days, km_this_week, medium_intensity_runs, high_intensity_runs, sunday_long_run)

        
        # Display the generated run schedule to the user
        if run_schedule is not None:
            st.header("Your PacePerfect Run Schedule")
            st.table(run_schedule)
        else:
            st.write("Error: Unable to generate the run schedule. Please make sure all fields are correct.")

if __name__ == "__main__":
    main_page()
