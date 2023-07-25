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

# create intensity function
# Maybe look at best fit line too and then take 20% above and below
def compute_relative_effort(run_pace, average_pace, distance, average_distance):
    # Calculate the effort score
    pace_multiplier = average_pace / run_pace
    distance_multiplier = distance / average_distance
    effort = 5 * pace_multiplier * distance_multiplier
    effort = np.clip(effort, 1, 10)

    return round(effort)

# Clip values above 10 and lower than 1
def clip_intensity(effort):
  # Set ceiling and floor for the effort level
  ceiling = 10  # Maximum effort level
  floor = 1     # Minimum effort level

  # Apply ceiling and floor constraints
  effort = np.clip(effort, floor, ceiling)

  return(effort)

def calculate_injury_likelihood(days_since_last_run, average_distance, average_pace):
    # Custom logic to calculate the injury likelihood score
    # You can use any formula or algorithm based on the input variables
    # For this example, let's use a simple formula as an illustration
    injury_score = days_since_last_run * 0.1 + average_distance * 0.5 + average_pace * 0.3
    injury_likelihood = min(100, max(0, injury_score))  # Cap the score between 0 and 100
    return injury_likelihood

def return_run_schedule(run_recommendations, number_of_days, weekly_target, medium_intensity_runs, high_intensity_runs, long_run):
    
    '''function to return optimized schedule of runs'''
    
    df = run_recommendations.head(7).reset_index()
    df['pace'] = '00:06:30'
    return df[['run_distance','pace']]

    
#EOF