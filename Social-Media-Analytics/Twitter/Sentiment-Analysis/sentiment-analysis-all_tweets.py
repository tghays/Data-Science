
# coding: utf-8

# In[1]:

from __future__ import absolute_import
from google.cloud import language
import google.cloud
import pandas as pd
import numpy as np
import tqdm
import operator
import facebook
import json
import tweepy
import time
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import datetime


#Create client instance for Google Natural Language API
client = language.Client()


# In[9]:

all_tweets_df = pd.DataFrame.from_csv('/Users/thays/Desktop/RDU_pitch/RDUpitch_ALL_tweets.csv', encoding='utf-8')
all_tweets_df.reset_index(inplace=True, drop = True)
all_tweets_df


# In[10]:

all_tweets_df[['brand', 'date']].groupby('brand').count()


# In[12]:

# Sentiment Analysis of Replies

sentiments_list = []
magnitudes_list = []
entities_name_list = []
entities_salience_list = []
comments = list(all_tweets_df['tweet'])

for comment in tqdm.tqdm(comments):

    try:
        document = client.document_from_text(comment)
        sentiment = document.analyze_sentiment()
        entities = document.analyze_entities()
        sentiment_score = sentiment.score
        magnitude = sentiment.magnitude
        entities_name = [str(x.name) for x in entities[:3]]
        entities_salience = [x.salience for x in entities[:3]]
    except UnicodeEncodeError:
        sentiment_score = None
        magnitude = [None]
        entities_name = [None]
        entities_salience = [None]


    sentiments_list.append(sentiment_score)
    magnitudes_list.append(magnitude)
    entities_name_list.append(entities_name)
    entities_salience_list.append(entities_salience)
    
    time.sleep(.2)
        
all_tweets_df['sentiment'] = sentiments_list
all_tweets_df['magnitude'] = magnitudes_list
all_tweets_df['entities'] = entities_name_list
all_tweets_df['entity_salience'] = entities_salience_list


# In[13]:

all_tweets_df.to_csv('/Users/thays/Desktop/RDU_pitch/RDUpitch_ALL_tweets_sentiment.csv', encoding='utf-8')


# In[14]:

all_tweets_df


# In[ ]:



