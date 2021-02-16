import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

def load_data():
    # Read in the datasets

    ''' Input: 
        Output: movies, reviews (Pandas Dataframe) '''

    df = pd.read_csv('data/user-item-interactions.csv')
    df_content = pd.read_csv('data/articles_community.csv')
    del df['Unnamed: 0']
    del df_content['Unnamed: 0']

    coded_dict = dict()
    cter = 1
    email_encoded = []
    
    for val in df['email']:
        if val not in coded_dict:
            coded_dict[val] = cter
            cter+=1
        
        email_encoded.append(coded_dict[val])

    del df['email']
    df['user_id'] = email_encoded

    return df, df_content