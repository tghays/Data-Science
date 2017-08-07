## Tweet Retrieval from Multiple Users

This script retrieves multiple tweets for different airports around the United States and saves the data in a Pandas DataFrame.  Queries are created with the airport Twitter handles:

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

This script uses [Tweepy](https://github.com/tweepy/tweepy) library to authenticate with the Twitter API and [Pandas](https://github.com/pandas-dev/pandas) to save the data.

<br>

A Pandas DataFrame is created to store the tweet, tweet meta-data, sentiment analysis metrics, and geospatial attributes:

```
df_tweets = pd.DataFrame(columns = ['date', 'time', 'location', 'handle', 'brand',\
                                    'tweet', 'posting_user', 'sentiment', 'magnitude', 'entities',\
                                    'entity_salience', 'geolocation', 'place', 'coordinates',])
```

<br>

An outer for loop is created to iterate through the airport handles.  A Tweepy Cursor is then used to iterate through the pages returned to the client.  If the API rate limit is reached, Tweepy will automatically wait the required 15 minutes until it sends another request to the Twitter servers:

```python
for tweet in tweepy.Cursor(api.search, q = '@' + handle, since = since, \
                           lang ='en', wait_on_rate_limit = True, \
                           wait_on_rate_limit_notify = True).items():
    tempTweetList.append(tweet)
```
