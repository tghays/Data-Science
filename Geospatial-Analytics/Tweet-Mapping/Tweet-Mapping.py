
# coding: utf-8

# In[61]:

import geopandas as gpd
import pandas as pd
import collections


# In[97]:

shp_file = '/Users/thays/Desktop/RDU_pitch/mapping/UScities/citiesx010g.shp'
shp_df = gpd.read_file(shp_file)
shp_df = shp_df[['NAME', 'COUNTY', 'STATE', 'STATE_FIPS', 'geometry']]
shp_df['NAME'] = shp_df['NAME'] + ', ' + shp_df['STATE']
shp_df.rename(columns = {'NAME':'city_state'}, inplace=True)


# In[98]:

shp_df.head()


# In[76]:

tweets_file = '/Users/thays/Desktop/RDU_pitch/RDU_Pitch_Location_Tweet Freq.csv'
tweets_df = pd.DataFrame.from_csv(tweets_file)
tweets_df.head()


# In[72]:

test_df = pd.DataFrame(columns = ['brand', 'city_state', 'freq'])
test_df['brand'] = tweets_df['city_state'] if tweets_df


# In[90]:

cityDict = {} #collections.OrderedDict()
# key = city, state : value = [brand, frequency value]

for idx, row in tweets_df.iterrows():
    city = row[1]
    if city in cityDict:
        if int(row[2]) > cityDict[city][1]:
            cityDict[city] = [row[0], row[2]]
        else:
            pass
    else:
        cityDict[city] = [row[0], row[2]]


# In[91]:

brand_list = []
city_list = []
freq_list = []

for key in cityDict:
    city_list.append(key)
    brand_list.append(cityDict[key][0])
    freq_list.append(cityDict[key][1])


# In[92]:

print (city_list[2], brand_list[2], freq_list[2])


# In[102]:

city_df = pd.DataFrame(columns=['city_state', 'brand', 'freq'])
city_df['city_state'] = city_list
city_df['brand'] = brand_list
city_df['freq'] = freq_list


# In[108]:

None in city_df


# In[122]:

map_df = gpd.GeoDataFrame.merge(shp_df, city_df, how = 'inner', on ='city_state')


# In[123]:

map_df


# In[124]:

map_df.to_file('/Users/thays/Desktop/RDU_pitch/mapping/tweetMap', driver='ESRI Shapefile')


# In[66]:

freq_list = list(map_df.frequency.unique())
freq_list.sort()


# In[128]:

AP_loc_list = list(map_df.brand.unique())


# In[134]:

AP_df = gpd.GeoDataFrame(columns =['city_state'])
AP_loc_list = ['Charlotte, NC',
 'Austin, TX',
 'Indianapolis, IN',
 'Atlanta, GA',
 'Nashville, TN',
 'Raleigh, NC',
 'San Diego, CA',
 'Portland, OR',
 'Louisville, KY']


# In[135]:

AP_df['city_state'] = AP_loc_list


# In[136]:

AP_map_df = gpd.GeoDataFrame.merge(shp_df, AP_df, how = 'inner', on ='city_state')


# In[139]:

AP_map_df.to_file('/Users/thays/Desktop/RDU_pitch/mapping/AP_locations', driver='ESRI Shapefile')


# In[140]:

map_df


# In[ ]:



