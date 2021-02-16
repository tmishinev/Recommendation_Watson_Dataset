import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle


# create the user-article matrix with 1's and 0's

def create_user_item_matrix(df):
    '''
    INPUT:
    df - pandas dataframe with article_id, title, user_id columns
    
    OUTPUT:
    user_item - user item matrix 
    
    Description:
    Return a matrix with user ids as rows and article ids on the columns with 1 values where a user interacted with 
    an article and a 0 otherwise
    '''
    # Fill in the function here
    user_item = df.groupby(['user_id', 'article_id']).agg(lambda x:1).unstack().fillna(0)
    
    return user_item # return the user_item matrix 


def get_article_names(article_ids, df):
    '''
    INPUT:
    article_ids - (list) a list of article ids
    df - (pandas dataframe) df as defined at the top of the notebook
    
    OUTPUT:
    article_names - (list) a list of article names associated with the list of article ids 
                    (this is identified by the title column)
    '''
    # Your code here
    # Your code here
    df_temp = df[['article_id', 'title']].drop_duplicates()

    article_names = []
    for x in article_ids:
        article_names.append(str(df_temp[df_temp['article_id']==float(x)]['title'].values[0]))
        
    return article_names # Return the article names associated with list of article ids


def get_user_articles(user_id, df, user_item):
    '''
    INPUT:
    user_id - (int) a user id
    user_item - (pandas dataframe) matrix of users by articles: 
                1's when a user has interacted with an article, 0 otherwise
    
    OUTPUT:
    article_ids - (list) a list of the article ids seen by the user
    article_names - (list) a list of article names associated with the list of article ids 
                    (this is identified by the doc_full_name column in df_content)
    
    Description:
    Provides a list of the article_ids and article titles that have been seen by a user
    '''
    # Your code here
    article_ids = list(df[df['user_id'] == user_id]['article_id'].astype('str'))
    article_names = list(df[df['user_id'] == user_id]['title'])
    
    return article_ids, article_names # return the ids and names


def get_top_sorted_users(user_id, df, user_item):
    '''
    INPUT:
    user_id - (int)
    df - (pandas dataframe) df as defined at the top of the notebook 
    user_item - (pandas dataframe) matrix of users by articles: 
            1's when a user has interacted with an article, 0 otherwise
    
            
    OUTPUT:
    neighbors_df - (pandas dataframe) a dataframe with:
                    neighbor_id - is a neighbor user_id
                    similarity - measure of the similarity of each user to the provided user_id
                    num_interactions - the number of articles viewed by the user - if a u
                    
    Other Details - sort the neighbors_df by the similarity and then by number of interactions where 
                    highest of each is higher in the dataframe
     
    '''

    # Your code here
    
    df_similarity = pd.DataFrame({'user_id' : user_item.index, 'similarity' : np.dot( user_item.loc[user_id, :], user_item.transpose())})

    df_similarity = df_similarity[df_similarity['user_id'] != user_id]

    df_interactions = df.groupby('user_id')['article_id'].count()

    neighbors_df = df_similarity.join(df_interactions, on = 'user_id').sort_values(['similarity','article_id'], ascending = [False, False])

    neighbors_df.rename(columns={"user_id": "neighbor_id", "article_id": "num_interactions"}, inplace = True)
    return neighbors_df # Return the dataframe specified in the doc_string


def user_user_recs_part2(user_id, df, user_item, m=10):
    '''
    INPUT:
    user_id - (int) a user id
    m - (int) the number of recommendations you want for the user
    
    OUTPUT:
    recs - (list) a list of recommendations for the user by article id
    rec_names - (list) a list of recommendations for the user by article title
    
    Description:
    Loops through the users based on closeness to the input user_id
    For each user - finds articles the user hasn't seen before and provides them as recs
    Does this until m recommendations are found
    
    Notes:
    * Choose the users that have the most total article interactions 
    before choosing those with fewer article interactions.

    * Choose articles with the articles with the most total interactions 
    before choosing those with fewer total interactions. 
   
    '''
    # Your code here
    
    recs = []
    most_similar_users = list(get_top_sorted_users(user_id, df, user_item)['neighbor_id'])
    user_articles, the_article_names = get_user_articles(user_id, df, user_item)
    for user in most_similar_users:
        article_ids, article_names = get_user_articles(user, df, user_item)
        for id in article_ids:
            if len(recs) < m and id not in user_articles and id not in recs:
                recs.append(id)
            else:
                break
        
        if len(recs) >= m:
                break
                
    rec_names = get_article_names(recs, df)
    print(len(recs))
    print(len(rec_names))
    df_recommendations = pd.DataFrame({'article_id': recs, 'title': rec_names})
    
    return df_recommendations