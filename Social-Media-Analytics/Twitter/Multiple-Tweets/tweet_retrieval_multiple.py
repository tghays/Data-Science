
# coding: utf-8

# In[4]:

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


# In[5]:

# Twitter Credentials

#Authentication Credentials
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'

access_token = 'access_token'
access_token_secret = 'access_token_secret'

#Twitter API Authorization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# In[26]:

main_handles = {'RDUairport' : 'RDU',
                'rduceo' : 'RDU',
                'CLTAirport' : 'Charlotte',
                'AUStinAirport' : 'Austin',
                'Fly_Nashville' : 'Nashville',
                'sdfariport' : 'Louisville',
                'flylouisville' : 'Louisville',
                'INDairport' : 'Indianapolis',
                'SanDiegoAirport' : 'San_Diego',
                'flypdx' : 'Portland',
                'atlairport' : 'Atlanta'}


# In[27]:

df_tweets = pd.DataFrame(columns = ['date', 'time', 'location', 'handle', 'brand',                                    'tweet', 'posting_user', 'sentiment', 'magnitude', 'entities',                                    'entity_salience', 'geolocation', 'place', 'coordinates',])


# In[28]:

# Get date list for last 10 days

date_list = []
start_date = (datetime.datetime.now() + datetime.timedelta(-10))
for i in range(10): 
    start_date += datetime.timedelta(days=1)
    date_str = start_date.strftime('%Y-%m-%d')
    date_list.append(date_str)
date_list


# In[29]:

since_date = (datetime.datetime.now() + datetime.timedelta(-9))
since = since_date.strftime('%Y-%m-%d')
since


# In[30]:

tweetDict = {}

# Understanding geolocation
geoDict = {}


# In[31]:


# Itereate through large handles
for handle_iter in tqdm.tqdm(main_handles.items()):
    
    handle = handle_iter[0]
    brand = handle_iter[1]
            
    tempTweetList = []

    # Get tweets for one handle, on one day
    for tweet in tweepy.Cursor(api.search, q = '@' + handle, since = since,                                lang ='en', wait_on_rate_limit = True,                                wait_on_rate_limit_notify = True).items():
        tempTweetList.append(tweet)
    tweetDict['tweets_' + handle] = tempTweetList

    tempTweetDateList = []
    tempTweetTimeList = []
    tempTweetLocationList = []
    tempTweetGeoList = []
    tempTweetPlaceList = []
    tempTweetCoordList = []
    tempTweetTextList = []
    tempTweetUserList = []
    tempTweetPostIDList = []
    tempTweetHandleList = []

    # Extract data from tweet objects
    for tweet_obj in tweetDict['tweets_' + handle]:
        tempTweetDateList.append(datetime.datetime.strftime(tweet_obj.created_at, '%Y-%m-%d'))
        tempTweetTimeList.append(str((tweet_obj.created_at).time()))
        tempTweetLocationList.append(tweet_obj.user.location)
        tempTweetGeoList.append(tweet_obj.geo)
        if tweet_obj.place:
            tempTweetPlaceList.append(tweet_obj.place.bounding_box.coordinates[0])
        else:
            tempTweetPlaceList.append(None)
        tempTweetCoordList.append(tweet_obj.coordinates)
        tempTweetTextList.append(tweet_obj.text)
        tempTweetUserList.append(tweet_obj.author.name)
        tempTweetPostIDList.append(tweet_obj.id)
        tempTweetHandleList.append('@' + handle)

        # Understanding Geolocation
        if tweet_obj.geo:
            geoDict[('geo', tweet_obj.id)] = tweet_obj.geo
        elif tweet_obj.place:
            geoDict[('place', tweet_obj.id)] = tweet_obj.place
        elif tweet_obj.coordinates:
            geoDict[('coord', tweet_obj.id)] = tweet_obj.coordinates
        else:
            pass

    temp_df = pd.DataFrame(columns = ['date', 'time', 'location', 'handle', 'brand',                                    'tweet', 'posting_user', 'sentiment', 'magnitude', 'entities',                                    'entity_salience', 'geolocation', 'place', 'coordinates',])
    temp_df['date'] = tempTweetDateList
    temp_df['time'] = tempTweetTimeList
    temp_df['location'] = tempTweetLocationList
    temp_df['handle'] = tempTweetHandleList
    temp_df['brand'] = brand
    temp_df['tweet'] = tempTweetTextList
    temp_df['posting_user'] = tempTweetUserList
    
    temp_df['geolocation'] = tempTweetGeoList
    temp_df['place'] = tempTweetPlaceList
    temp_df['coordinates'] = tempTweetCoordList

    df_tweets = pd.concat([df_tweets, temp_df])

    df_tweets.to_csv('/Users/thays/Desktop/RDU_pitch/RDU_pitch_{0}_tweets.csv'.format(brand), encoding='utf-8')
    


# ## Testing Functionality

# In[ ]:

query = 'ECUAthletics'
tempTweetList = []
for ix, date_query in enumerate(date_list):    
    since = date_query
    if ix != len(date_list) - 1:
        until = date_list[ix + 1]
    else:
        until = date_query
        
    for tweet in tweepy.Cursor(api.search, q = '@' + query, since = since, until = until,                                 wait_on_rate_limit = True,                                wait_on_rate_limit_notify = True).items():
        tempTweetList.append(tweet)
        print ('iteration')

