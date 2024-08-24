# -*- coding: utf-8 -*-
"""
Streamlit version
@author: Matt Pitz
"""

#libraries
import json
import numpy as np
import pandas as pd
from datetime import datetime as dt
from surprise import Dataset, Reader
from surprise import SVD
from surprise.model_selection import cross_validate
from datetime import timedelta
from itertools import combinations


def generate_run_ratings(filtered_df,user_id, weekly_target, number_of_days):
    #global filtered_df,user_id, weekly_target, number_of_days
    long_run_multiple = 3
    
    """
    Trains a SVD recommender and generates a list of run distances with ratings based on weekly target, 
    number of days run each week, with an optional param that sets the upper bound long run distance
    """

    #load in best hyperparameters
    with open('svdauto_tune_results.json') as json_file:
        parameters = json.load(json_file)
    parameters.pop('algo')
    parameters.pop('rmse')

    data = Dataset.load_from_df(filtered_df[["user_id","run_distance_rounded","weekly_frequency"]], Reader(rating_scale=(0,7)))

    #build model with cross validation
    algo = SVD(verbose=False, lr_bi = parameters['lr_bi'], lr_bu = parameters['lr_bu'], lr_pu = parameters['lr_pu'], lr_qi = parameters['lr_qi'], 
               n_epochs = parameters['n_epochs'], n_factors = parameters['n_factors'], reg_bi= parameters['reg_bi'], reg_bu = parameters['reg_bu'], 
               reg_pu = parameters['reg_pu'], reg_qi = parameters['reg_qi'])
    cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=False)

    
    #create list of run lengths
    run_list = range(round(weekly_target/(number_of_days+(long_run_multiple-1))), round((weekly_target/number_of_days) * long_run_multiple))
    results_dict = {'run_distance': [],
                   'run_rating': []}
    
    #generate list of recommended runs
    for run in run_list:
        rating_prediction = algo.predict(uid = user_id, iid = run)[3]
        results_dict['run_distance'].append(run)
        results_dict['run_rating'].append(rating_prediction)
        
    return pd.DataFrame(results_dict).sort_values(by=['run_rating'], ascending = False)


def convert_timedelta_to_minutes(timedelta_value):
    # Convert a timedelta object to minutes
    return timedelta_value.total_seconds() / 60


def adjust_pace_based_on_intensity(pace, intensity):
    if intensity == 'high':
        return pace * 0.95  # Decrease pace by 5% for high-intensity run
    elif intensity == 'medium':
        return pace * 0.98  # Decrease pace by 2% for medium-intensity run
    else:
        return pace  # No adjustment for other runs

# Function to generate the intensity for each run based on user input
def generate_intensity_schedule(num_medium_runs, num_high_runs, num_runs):
    run_types = ['low'] * (num_runs - num_medium_runs - num_high_runs)
    run_types.extend(['medium'] * num_medium_runs)
    run_types.extend(['high'] * num_high_runs)
    return run_types

def convert_float_minutes_to_time(float_minutes):
    # Convert float in minutes to time in 'HH:MM:SS' format

    hours = int(float_minutes // 60)
    minutes = int(float_minutes % 60)
    seconds = int((float_minutes % 1) * 60)

    time_formatted = f"{hours:02}:{minutes:02}:{seconds:02}"
    return time_formatted

def calculate_injury_likelihood(days_since_last_run, average_distance, average_pace):
    # Custom logic to calculate the injury likelihood score
    # You can use any formula or algorithm based on the input variables
    # For this example, let's use a simple formula as an illustration
    injury_score = days_since_last_run * 0.1 + average_distance * 0.5 + average_pace * 0.3
    injury_likelihood = min(100, max(0, injury_score))  # Cap the score between 0 and 100
    return injury_likelihood

def return_run_schedule(recommendations_df, number_of_days, weekly_target, medium_intensity_runs, high_intensity_runs, long_run):
    #global recommendations_df, number_of_days, weekly_target, medium_intensity_runs, high_intensity_runs, long_run
    '''
    function to return optimized schedule of runs
    
    1) Duplicates high rating runs
    2) Selects set whose combination is somewhat close to target with highest ratings
    3) Increases/decreases individual runs to match target
    4) Sorts results with longest run at the end, 2nd longest in the middle to provide well spaced runs
    ***
    5) Sets pace
    6) Adjusts for medium/high intenstiy run requests
    7) Checks for long run. If current one is not long enough, puts it at the end of the week
    ***
    
    8) Returns schedule
    '''
    df = recommendations_df
    
    ## 1 ##
    # expand rating dataframe for runs with high ratings
    df_high_ratings = df[df['run_rating'] >= 1.4]
    
    df = pd.concat([df_high_ratings,df])
    
    #Next reduce the set of runs
    df = df.head(15)
    
    ## 2 ##
    # Select runs equal to number_of_days with highest combined rating close to target km
    
    # Calculate the lower and upper bounds for the selection
    lower_bound = weekly_target - 0.2 * weekly_target
    upper_bound = weekly_target + 0.2 * weekly_target
    
    # Initialize vars for combinations
    best_combination = None
    best_rating = 0
    
    # Generate all combinations of distances for target days
    for combination in combinations(df.itertuples(index=False), number_of_days):
        total_distance = sum(x.run_distance for x in combination)
        total_rating = sum(x.run_rating for x in combination)

        # Check if the total distance is within the bounds and if the total rating is better than the best so far
        if lower_bound <= total_distance <= upper_bound and total_rating > best_rating:
            best_combination = combination
            best_rating = total_rating
   
    # Create dataframe with best set of runs/ratings
    df_runs = pd.DataFrame(best_combination, columns=df.columns)
    
    #if no results, take top runs equal to the number_of_days
    if (df_runs.size == 0):
        df_runs = df.head(number_of_days)
    
    ## 3 ##
    #Adjust distances to match desired weekly target, starting with lowest rated runs
    df_runs = df_runs.sort_values('run_rating', ascending=True)
    
    # Calculate the current sum of distances
    current_sum = df_runs['run_distance'].sum()
    
    # Loop until the current sum equals 'weekly_target'
    while current_sum != weekly_target:
        # Loop through each row
        for i, row in df_runs.iterrows():
            # If the current sum is less than 'weekly_target', increment the distance
            if current_sum < weekly_target:
                df_runs.loc[i, 'run_distance'] += 1
                current_sum += 1
            # If the current sum is greater than 'weekly_target', decrement the distance
            elif current_sum > weekly_target and df_runs.loc[i, 'run_distance'] > 3:
                df_runs.loc[i, 'run_distance'] -= 1
                current_sum -= 1
            
            # If the current sum equals 'weekly_target', break the loop
            if current_sum == weekly_target:
                break
                
    ## 4 ##
    #Shuffle the runs, then sort longest run to last and 2nd longest to middle
    df_runs = df_runs.sample(frac = 1)
    
    #create index column
    df_runs = df_runs.assign(index=range(1,len(df_runs)+1))
    
    #Find longest and 2nd longest runs
    max_distance = df_runs['run_distance'].max()
    second_longest_distance = df_runs[df_runs['run_distance'] < max_distance]['run_distance'].max()
    
    #set index for runs
    df_runs.loc[df_runs['run_distance'] == max_distance, 'index'] =  df_runs['index'].max() + 1
    df_runs.loc[df_runs['run_distance'] == second_longest_distance, 'index'] =  df_runs['index'].mean() + .1
    
    #sort by index and drop index
    df_runs = df_runs.sort_values('index', ascending=True)
    df_runs = df_runs.drop(columns = ['index'])
    
    
    ## 5 ##
    # Set pace
    # Average Pace for everyone
    average_pace = 9
    
    # Average Distance for everyone
    average_distance = 7
    
    # Distance multiplier (from intensity score); 0.1 is to dampen results
    df_runs['pace_adjusted'] = average_pace * (1 + ( 0.1 * (df_runs['run_distance'] / average_distance)))
    
    ## 6 ##
    #adjust for medium intensity
    #adjust for high intensity
    
    df_runs['intensity'] = generate_intensity_schedule(medium_intensity_runs, high_intensity_runs, number_of_days)
    
    # Sort the DataFrame by intensity in descending order
    df_runs = df_runs.sort_values('intensity', ascending=False)

    # Set a floor and ceiling on pace
    floor_pace = 5  # 00:05:00 in seconds
    ceiling_pace = 15  # 00:15:00 in seconds
    df_runs['pace_adjusted'] = df_runs['pace_adjusted'].apply(lambda x: min(max(x, floor_pace), ceiling_pace))

    # Convert the smoothed pace to the 'HH:MM:SS' format
    df_runs['pace'] = df_runs['pace_adjusted'].apply(convert_float_minutes_to_time)

    # Adjust pace based on intensity
    df_runs['pace_adjusted'] = df_runs.apply(lambda row: adjust_pace_based_on_intensity(row['pace_adjusted'], row['intensity']), axis=1)

    # Convert the adjusted pace to the 'HH:MM:SS' format
    df_runs['pace'] = df_runs['pace_adjusted'].apply(convert_float_minutes_to_time)
    
    ## 7 ##
    
    # If long run multiply distance by 1.5
    if long_run == 'Yes':
        df_runs.loc[df_runs.index[-1], 'run_distance'] *= 1.5
    
    ## 8 ##
    #return schedule
    df_runs = df_runs[['run_distance', 'pace']].rename(columns={'run_distance': 'Run Distance', 'pace': 'Pace'})
    # Remove the index and return only the 'Run Distance' and 'Pace' columns
    #return df_runs.to_string(index=False)
    return df_runs
   
    
    #return df_runs[['run_distance','pace']]

    
#EOF