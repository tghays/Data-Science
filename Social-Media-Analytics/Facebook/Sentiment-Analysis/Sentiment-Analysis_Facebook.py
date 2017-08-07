
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


# In[2]:

fb_comments_df = pd.DataFrame.from_csv('/Users/thays/Desktop/RDU_pitch/RDUpitch_all_fb_comments.csv', encoding='utf-8')
fb_comments_df.reset_index(inplace=True, drop = True)
fb_comments_df


# In[3]:

# Sentiment Analysis of Replies

reply_sentiments_list = []
reply_magnitudes_list = []
reply_entities_name_list = []
reply_entities_salience_list = []
post_sentiments_list = []
post_magnitudes_list = []
post_entities_name_list = []
post_entities_salience_list = []

comments_list = list(zip(fb_comments_df['reply_comment_text'], fb_comments_df['post_text']))

for comment_iter in tqdm.tqdm(comments_list):
    
    comment = comment_iter[0]
    post = comment_iter[1]

    # Comment sentiment analysis
    try:
        reply_document = client.document_from_text(comment)
        reply_sentiment = reply_document.analyze_sentiment()
        reply_entities = reply_document.analyze_entities()
        reply_sentiment_score = reply_sentiment.score
        reply_magnitude = reply_sentiment.magnitude
        reply_entities_name = [str(x.name) for x in reply_entities[:3]]
        reply_entities_salience = [x.salience for x in reply_entities[:3]]
    except UnicodeEncodeError:
        sentiment_score = None
        magnitude = [None]
        entities_name = [None]
        entities_salience = [None]

    # Post sentiment analysis
    try:
        post_document = client.document_from_text(post)
        post_sentiment = post_document.analyze_sentiment()
        post_entities = post_document.analyze_entities()
        post_sentiment_score = post_sentiment.score
        post_magnitude = post_sentiment.magnitude
        post_entities_name = [str(x.name) for x in post_entities[:3]]
        post_entities_salience = [x.salience for x in post_entities[:3]]
    except UnicodeEncodeError:
        post_sentiment_score = None
        post_magnitude = [None]
        post_entities_name = [None]
        post_entities_salience = [None]


    reply_sentiments_list.append(reply_sentiment_score)
    reply_magnitudes_list.append(reply_magnitude)
    reply_entities_name_list.append(reply_entities_name)
    reply_entities_salience_list.append(reply_entities_salience)

    post_sentiments_list.append(post_sentiment_score)
    post_magnitudes_list.append(post_magnitude)
    post_entities_name_list.append(post_entities_name)
    post_entities_salience_list.append(post_entities_salience)
    
fb_comments_df['reply_sentiment'] = reply_sentiments_list
fb_comments_df['reply_magnitude'] = reply_magnitudes_list
fb_comments_df['reply_entities'] = reply_entities_name_list
fb_comments_df['reply_entity_salience'] = reply_entities_salience_list

fb_comments_df['post_sentiment'] = post_sentiments_list
fb_comments_df['post_magnitude'] = post_magnitudes_list
fb_comments_df['post_entities_name'] = post_entities_name_list
fb_comments_df['post_entity_salience'] = post_entities_salience_list


# In[4]:

fb_comments_df.to_csv('/Users/thays/Desktop/RDU_pitch/RDUpitch_all_fb_comments_sentiment.csv', encoding='utf-8')


# In[ ]:



