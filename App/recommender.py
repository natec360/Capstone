# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 20:32:30 2023

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
from itertools import combinations


def generate_run_ratings(filtered_df,user_id, weekly_target, number_of_days, long_run_multiple = 3):

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


def return_run_schedule(run_recommendations, number_of_days, weekly_target, medium_intensity_runs, high_intensity_runs, long_run):
    
    '''
    function to return optimized schedule of runs
    
    1) Duplicates high rating runs
    2) Selects set whose combination is somewhat close to target with highest ratings
    3) Increases/decreases individual runs to match target
    4) Sorts results with longest run at the end, 2nd longest in the middle to provide well spaced runs
    
    NOT IMPLEMENTED
    ***
    5) Sets pace
    6) Adjusts for medium/high intenstiy run requests
    7) Checks for long run. If current one is not long enough, puts it at the end of the week
    ***
    
    8) Returns schedule
    '''
    df = run_recommendations
    
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
            elif current_sum > weekly_target:
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
    #set pace
    df_runs['pace'] = '00:06:30'
    
    ## 6 ##
    #adjust for medium intensity
    
    ## 7 ##
    #adjust for high intensity
    
    
    ## 8 ##
    #return schedule 
    return df_runs[['run_distance','pace']]

    
#EOF