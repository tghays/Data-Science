
# coding: utf-8

# ## Example of a request to Google Analytics 

# The request includes metrics of 'sessions' and 'users' and geographic dimensions to enable future mapping of the metrics.
# 
# Pandas io module was used to send the request and retrieve the data in a pandas dataframe.

# In[13]:

import pandas.io.ga as ga
import pandas as pd
import datetime
import time


# In[14]:

account_id = 'account_id'
property_id = 'UA-property_id-xx'
view_id = 'view_id'


start_date = '2016-01-01'
end_date = '2017-01-01'


dimensions = ['date',
              'cityId',
              'city']

# Metrics for Request
metrics = ['sessions',
           'users']

tempStartTime = start_date

count = 0
while str(tempStartTime) <= end_date:
    temp_df = ga.read_ga(
                     account_id  = account_id,
                     profile_id  = view_id, 
                     property_id = property_id,
                     metrics     = metrics, 
                     dimensions  = dimensions, 
                     start_date  = tempStartTime, 
                     end_date    = today, 
                     index_col   = 0)

    tempStartTime = temp_df.index.max()
    
    if count == 0:
        df = temp_df
    else:
        df = pd.concat([df,temp_df])
    count+=1
    time.sleep(.2)


# In[22]:

test = df.sort(['sessions'], ascending=[False])
test


# In[ ]:



