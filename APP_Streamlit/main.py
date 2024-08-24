# main.py

from recommender import generate_run_ratings, return_run_schedule
from get_user_data import get_user_data, get_run_plan
import database_utils as dbf


def main(new_user, user_id, gender, age_group, month, updated_user_df, km_this_week, days_to_run, medium_intensity_runs, high_intensity_runs, sunday_long_run):
    # Collect user inputs (note only works for new users for now)
    #new_user, user_id, gender, age_group, month, updated_user_df = user.get_user_data()
    new_user, user_id, gender, age_group, month, updated_user_df = get_user_data()


    # Collect user goals
    #weekly_target, days_to_run, medium_intensity_runs, high_intensity_runs, long_run = user.get_run_plan()
    weekly_target, days_to_run, medium_intensity_runs, high_intensity_runs, long_run = get_run_plan()


    # Load the database in memory (Move this to server start when website work)
    raw_df = dbf.load_data()
    print('Finished loading.')

    # Pass user data to the database
    update_user_df = dbf.update_database(new_user, gender, age_group, month, weekly_target, days_to_run, user_id, updated_user_df)

    # Create dataset with user data for the model
    filtered_df = dbf.database_for_recommender(raw_df, update_user_df, gender, age_group, month, days_to_run, weekly_target)

    # Return recommendations
    recommendations_df = generate_run_ratings(filtered_df, user_id, weekly_target, days_to_run)

    # Return training plan
    run_schedule = return_run_schedule(recommendations_df, days_to_run, weekly_target, medium_intensity_runs, high_intensity_runs, long_run)

    return run_schedule
