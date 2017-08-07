# Twitter Location Retrieval

This script retrieves the location for a specified user.  Due to the fact that about 90% of tweets we were retrieving did not have any geodata enabled, we used the location of the user as a proxy.  To determine the location of the user, the user's followers were iterated through, and the location of the user was appended to a list.  The location that occurs msot commonly in the list was determined to be the user's location.

Iterate through the pages containing followers for the specified handle, through a Tweepy Cursor
```python
for user in tweepy.Cursor(api.followers, id='UNC_Basketball').pages():
    users.append(user)
```

Iterate through the pages returned in users list, then iterate through the followers of the users, appending the location of the user's follower's location to a list.
```python
locations = []
for page in users:
    for follower in page['users']:
        if follower['location'] != '':
            locations.append(follower['location'])
```

Retrieve the maxmially occuring location of the followers.
```python
max(set(locations), key=locations.count)
```


*This approach assumes most of followers of a specific Twitter handle will coincide geographically to the handle's location.*
