
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
import dateutil.parser as dateparser


#Create client instance for Google Natural Language API
client = language.Client()


# In[2]:

# Facebook Credentials

FB_APP_ID = 'FB_APP_ID'
FB_APP_SECRET = 'FB_APP_SECRET'

USER_ID = 'USER_ID'

USER_TOKEN= 'USER_TOKEN'
FB_TOKEN = 'FB_TOKEN'

# Facebook Graph API
graph = facebook.GraphAPI(access_token=FB_TOKEN, version='2.2')

#graph.extend_access_token(FB_APP_ID, FB_APP_SECRET)


# In[4]:

since = '2017-02-26'
until = '2017-03-07'


# In[5]:

fb_comments_df = pd.DataFrame(columns = ['reply_comment_date', 'reply_comment_time', 'reply_comment_text',                                           'reply_comment_id', 'reply_username', 'reply_user_id', 'brand', 'post_date',                                          'post_time', 'post_text', 'post_id'])


# In[6]:

brand_id = '123456789'
brand = 'RDU'

temp_post_objects = graph.get_connections(brand_id, 'posts', since = since, until = until)
temp_posts = {}
while(True):
    try:
        for temp_post_object in temp_post_objects['data']:
            temp_posts[(temp_post_object['id'], dateparser.parse(temp_post_object['created_time']))] = temp_post_object['message'] 
        temp_post_objects = requests.get(temp_post_object['paging']['next']).json()
    except KeyError:
        break

temp_fb_comments_df = pd.DataFrame(columns = ['reply_comment_date', 'reply_comment_time', 'reply_comment_text',                                       'reply_comment_id', 'reply_username', 'reply_user_id', 'brand', 'post_date',                                      'post_time', 'post_text', 'post_id'])

for post_meta in temp_posts:

    # Get datetime of the UF post
    post_datetime = post_meta[1]
    post_date = str(post_datetime.date())
    post_time = str(post_datetime.time())
    post_text = temp_posts[post_meta]
    post_id = post_meta[0]

    reply_comment_date_list = []
    reply_comment_time_list = []
    reply_comment_text_list = []
    reply_comment_id_list = []
    reply_user_name_list = []
    reply_user_id_list = []

    #user_commenter_ageRange_list = []
    #user_commenter_education_list = []
    #user_commenter_gender_list = []
    #user_commenter_location_list = []

    # Start initial comments object for iteration; all comments under post, including pagination info
    comments = graph.get_connections(post_id, 'comments')
    while(True):
        try:
            for comment in comments['data']:
                reply_comment_date_list.append(str(dateparser.parse(comment['created_time']).date()))
                reply_comment_time_list.append(dateparser.parse(str(dateparser.parse(comment['created_time']).time())))
                reply_comment_text_list.append(comment['message'])
                reply_comment_id_list.append(comment['id'])
                reply_user_name_list.append(comment['from']['name'])
                reply_user_id_list.append(comment['from']['id'])

                # Get commenter's location
                #user_commenter_id = comment['from']['id']
                #user_commenter_profile = graph.get_object(user_commenter_id)

            commments = requests.get(comment['paging']['next']).json()
        except KeyError:
            break

    temp_df = pd.DataFrame(columns = ['reply_comment_date', 'reply_comment_time', 'reply_comment_text',                                       'reply_comment_id', 'reply_username', 'reply_user_id', 'brand', 'post_date',                                      'post_time', 'post_text', 'post_id'])

    temp_df['reply_comment_date'] = reply_comment_date_list
    temp_df['reply_comment_time'] = reply_comment_time_list
    temp_df['reply_comment_text'] = reply_comment_text_list
    temp_df['reply_comment_id'] = reply_comment_id_list
    temp_df['reply_username'] = reply_user_name_list
    temp_df['reply_user_id'] = reply_user_id_list
    temp_df['brand'] = brand
    temp_df['post_date'] = post_date
    temp_df['post_time'] = post_time
    temp_df['post_text'] = post_text
    temp_df['post_id'] = post_id

    temp_fb_comments_df = pd.concat([temp_fb_comments_df, temp_df])

fb_comments_df = pd.concat([fb_comments_df, temp_fb_comments_df])


# In[7]:

fb_comments_df


# In[8]:

fb_comments_df.to_csv('/Users/thays/Desktop/RDU_pitch/RDUpitch_all_fb_comments.csv', encoding='utf-8')


# In[ ]:



