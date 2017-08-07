
# coding: utf-8

# In[65]:

import tweepy
import pandas as pd


# In[66]:

# Twitter Credentials

#Authentication Credentials
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'

access_token = 'access_token'
access_token_secret = 'access_token_secret'

#Twitter API Authorization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# In[ ]:

users = []
count = 0
for user in tweepy.Cursor(api.followers, id='UNC_Basketball').pages():
    users.append(user)


# In[68]:

locations = []
for page in users:
    for follower in page['users']:
        if follower['location'] != '':
            locations.append(follower['location'])


# In[71]:

len(locations)


# In[70]:

max(set(locations), key=locations.count)


# In[ ]:



