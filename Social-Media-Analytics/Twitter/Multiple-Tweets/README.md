## Tweet Retrieval from Multiple Users

This script retrieves multiple tweets for different airports around the United States and saves the data in a Pandas DataFrame.

```
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

This script uses [Tweepy](https://github.com/tweepy/tweepy) library to authenticate with the Twitter API and [Pandas](https://github.com/pandas-dev/pandas) to save the data.
