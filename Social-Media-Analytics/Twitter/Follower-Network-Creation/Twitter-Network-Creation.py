
# coding: utf-8

# # Follower Network Creation - Twitter Scrape

# This script references a previously

# In[ ]:

import os
import urllib
import tqdm
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from IPython.display import clear_output


# ### Path to the web driver for Firefox

# In[ ]:

gecko_path = '/Users/thays/anaconda/envs/python2.7/lib/python2.7/site-packages/selenium'


# ### Twitter URL to scrape
# This URL was previously referenced to obtain an initial list of followers for UNC_Basketball

# In[2]:

# define specific url for the semester
url = "https://twitter.com/UNC_Basketball/followers"


# ### Define the scrolling function
# This function scrolls to the end of the page waiting for changes in page loading.  A simple sleep (wait) function is used to wait for the page to load, which is variable based on connection speed.  A more efficient approach would be to check if the loading gif image was present in the page, and adjust functionality accordingly.

# In[3]:

def scrollDown(browser, numberOfScrollDowns):
    body = browser.find_element_by_tag_name("body")
    x = 0
    while numberOfScrollDowns >=0:
        targets_before_objs = browser.find_elements_by_class_name("u-linkComplex-target")
        targets_before = [i for i in targets_before_objs if i.text != '']
        if x == 0:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(.5)
            body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        numberOfScrollDowns -= 1
        time.sleep(.2)
        if numberOfScrollDowns % 10 == 0:
            print 'remaining scroll downs: {}'.format(numberOfScrollDowns)
        targets_after_objs = browser.find_elements_by_class_name("u-linkComplex-target")
        targets_after = [i for i in targets_after_objs if i.text != '']
        
        added = len(targets_after) - len(targets_before)
        clear_output()
        print ('Total followers = {}'.format(len(targets_before)))
        print ('added {}'.format(added))
        
        if added == 0:
            print ('None added, pausing for .2')
            time.sleep(.2)
            targets_after_objs = browser.find_elements_by_class_name("u-linkComplex-target")
            targets_after = [i for i in targets_after_objs if i.text != '']
            
            if len(targets_after) == len(targets_before):
                print ('None added, pausing for .5')
                time.sleep(.5)
                targets_after_objs = browser.find_elements_by_class_name("u-linkComplex-target")
                targets_after = [i for i in targets_after_objs if i.text != '']
                
                if len(targets_after) == len(targets_before):
                    print ('None added, pausing for 1')
                    time.sleep(1)
                    targets_after_objs = browser.find_elements_by_class_name("u-linkComplex-target")
                    targets_after = [i for i in targets_after_objs if i.text != '']
      
                    if len(targets_after) == len(targets_before):
                        print ('No more follower links to load, terminating')
                        break           
                else:
                    print ('added {}'.format(len(targets_after) - len(targets_before)))
                    
            else:
                print ('added {}'.format(len(targets_after) - len(targets_before)))
                
            
    return browser, targets_before, targets_after


# In[4]:

sm_follower_ids_df = pd.DataFrame.from_csv('/Users/thays/Desktop/twitter_influencer_search_engine/sm_followers.csv')
sm_followers_ids = list(sm_follower_ids_df['follower'])


# In[5]:

main_df = pd.DataFrame(columns = ['user', 'follower'])


# In[6]:

sm_followers_ids_test = sm_followers_ids[:10]


# In[8]:

# define webdriver
driver = webdriver.Firefox()
driver.get(url)
count = 0

username = driver.find_element_by_class_name("js-username-field")
password = driver.find_element_by_class_name("js-password-field")

username.send_keys("username")
password.send_keys("password")
driver.find_element_by_css_selector("button.submit.btn.primary-btn").click()
time.sleep(2)

follower_count = 1

for sm_follower_id in sm_followers_ids_test:

    driver.get('https://twitter.com/intent/user?user_id={}'.format(sm_follower_id))

    link_objs = driver.find_elements_by_class_name('alternate-context')
    links =[]
    for link in link_objs:
        links.append(link.get_property('href'))
    followers_link = next(i for i in links if 'followers' in i)
    handle = followers_link.split('/')[-2]
    driver.get(followers_link)
    time.sleep(.5)
    
    browser = scrollDown(driver, 2000)
    all_targets_objs = driver.find_elements_by_class_name("u-linkComplex-target")[12:]
    all_targets = [i for i in all_targets_objs if i.text != '']
    temp_df = pd.DataFrame(columns = ['user', 'follower'])
    
    temp_followers = []
    for a_target in all_targets:
        temp_followers.append(a_target.text)
    temp_users = [handle] * len(temp_followers)
    
    temp_df['user'] = temp_users
    temp_df['follower'] = temp_followers
    
    main_df = main_df.append(temp_df)
    
    follower_count += 1
    print ('follower {} complete'.format(follower_count))


# In[9]:

main_df


# In[ ]:



