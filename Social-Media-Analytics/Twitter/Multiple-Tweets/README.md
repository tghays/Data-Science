## Tweet Retrieval from Multiple Users

This script retrieves multiple tweets for different airports around the United States and saves the data in a Pandas DataFrame.  Queries are created with the Twitter handles for each airport:

```python
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
```

## How it works

This script uses [Tweepy](https://github.com/tweepy/tweepy) library to authenticate with the Twitter API and [Pandas](https://github.com/pandas-dev/pandas) to save the data.  For safe data storage, a unique csv is saved with tweet data for each airport, the csv's are later combined for future analysis.

A Pandas DataFrame is created to store the tweet, tweet meta-data, sentiment analysis metrics, and geospatial attributes:

```
df_tweets = pd.DataFrame(columns = ['date', 'time', 'location', 'handle', 'brand',\
                                    'tweet', 'posting_user', 'sentiment', 'magnitude', 'entities',\
                                    'entity_salience', 'geolocation', 'place', 'coordinates',])
```


An outer for loop is created to iterate through the airport handles.  A Tweepy Cursor is then used to iterate through the pages returned to the client.  For each iteration within the Tweepy Cursor, the "item page" is appended to a list.  That list is then assigned to a dictionary key of the specified handle. If the API rate limit is reached, Tweepy will automatically wait the required 15 minutes until it sends another request to the Twitter servers:

```python
for tweet in tweepy.Cursor(api.search, q = '@' + handle, since = since, \
                           lang ='en', wait_on_rate_limit = True, \
                           wait_on_rate_limit_notify = True).items():
    tempTweetList.append(tweet)
tweetDict['tweets_' + handle] = tempTweetList
```

Lists for each DataFrame column are created, and upon completing the iteration for a unique airport, the list is assigned to the appropriate DataFrame column.  For each iteration of the outer for-loop, these lists are over-written, redifined again.

```python
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
```


In the tweet list (stored in the dictionary key) for a specific airport are json objects.  These objects are iterated through and relevant data is retrieved and appended to the corresponding list.  If geographic data is included for the tweet, this information is appended to a geo dictionary (geoDict).  These lists are then assigned to the DataFrame column, and the DataFrame is exported to a csv file, with utf-8 encoding.
```python
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

temp_df = pd.DataFrame(columns = ['date', 'time', 'location', 'handle', 'brand',\
                                'tweet', 'posting_user', 'sentiment', 'magnitude', 'entities',\
                                'entity_salience', 'geolocation', 'place', 'coordinates',])
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
```


