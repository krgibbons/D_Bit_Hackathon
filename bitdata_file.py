# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 19:54:12 2021

@author: kgibbons
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import math
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split


historical_reddit_data = pd.read_csv('subredditdata.csv')
historical_prices_data = pd.read_csv('historicalprices.csv')

def breakup_by_date(data):
    breakpoints= []
    dataframes = []
    current_index_time = datetime(2018,7,24,16,55)
    new_date = current_index_time
    target_date = new_date + timedelta(days=1)
        
    for index,val in enumerate(data['CREATED_UTC'].to_list()):
         if datetime.strptime(val, '%Y-%m-%d %H:%M:%S') < target_date:
             continue
         else:
             breakpoints.append(index)
             target_date = target_date + timedelta(days=1)
             
    for index, item in enumerate(breakpoints):
        if index == 0:
            abridged_dataframe = data.iloc[0:item]
            dataframes.append(abridged_dataframe)
        
        else:
            abridged_dataframe = data.iloc[breakpoints[index-1]:item]
            dataframes.append(abridged_dataframe)
            
    return dataframes
        

              
    
dataframes = breakup_by_date(historical_reddit_data)

dataframes.pop(-1)

analyzer = SentimentIntensityAnalyzer()

def generate_prices_delta(pricesdata):
    delta_list = []
    pricelist= pricesdata['CLOSE'].iloc[570:].to_list()
    for index, entry in enumerate(pricelist):
        try:
            pricedelta = pricelist[index+1] - entry
            delta_list.append(pricedelta)
        except IndexError: 
            break
    return delta_list
    
hmm = historical_prices_data['CLOSE'].iloc[570:].to_list()  
outputs = generate_prices_delta(historical_prices_data)             
                
        

def prepare_data(data):
    new_dataframes = []
    for dataframe in data:
        dataframe['compound'] = [analyzer.polarity_scores(x)['compound'] for x in dataframe['TITLE']]
        dataframe['neg'] = [analyzer.polarity_scores(x)['neg'] for x in dataframe['TITLE']]
        dataframe['neu'] = [analyzer.polarity_scores(x)['neu'] for x in dataframe['TITLE']]
        dataframe['pos'] = [analyzer.polarity_scores(x)['pos'] for x in dataframe['TITLE']]
        new_dataframes.append(dataframe)
    return new_dataframes

lol = prepare_data(dataframes)

def prepare_input_vector(data):
    vectors = []
    for item in data:
        avg_compound = item['compound'].mean()
        avg_neg = item['neg'].mean()
        avg_neu = item['neu'].mean()
        avg_pos = item['pos'].mean()
        number_of_posts = len(item.index)
        vector = [avg_compound, avg_neg, avg_pos, number_of_posts]
        vectors.append(vector)
    return vectors

to_feed = prepare_input_vector(lol)

X_train, X_test, y_train, y_test = train_test_split(
    to_feed, outputs, test_size=0.33, random_state=42)
