# Sentiment Analysis

This script uses the tweets retrieved from the "Multiple Tweets" script in a combined csv and runs a sentiment analysis on the tweets using the Google Natural Language Processing library. 


## How it works
A connection must be made to Google's Natural Language Cloud API, this method references a "client_secrets.json" in the directory where the library is stored.
```python
client = language.Client()
```

Retrieve the tweets from a csv using Pandas
```python
all_tweets_df = pd.DataFrame.from_csv('/Users/thays/Desktop/RDU_pitch/RDUpitch_ALL_tweets.csv', encoding='utf-8')
all_tweets_df.reset_index(inplace=True, drop = True)
```

Get the number of tweets for each airport
```python
all_tweets_df[['brand', 'date']].groupby('brand').count()
```

Run the sentiment analysis, iterating through a list of "comments" (tweets), retrieved from the "tweet" column of the DataFrame.  tqdm is used here for informative output on the progress of the loop.
```python
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
```

Save final DataFrame to csv
```python
all_tweets_df.to_csv('/Users/thays/Desktop/RDU_pitch/RDUpitch_ALL_tweets_sentiment.csv', encoding='utf-8')
```
