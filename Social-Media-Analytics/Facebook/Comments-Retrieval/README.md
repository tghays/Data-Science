# Facebook Comments Retrieval

This script retrieves comments for a specified Facebook user, using Facebook's Graph API.

## How it works

A connection to Facebook's Graph API is made
```python
FB_APP_ID = 'FB_APP_ID'
FB_APP_SECRET = 'FB_APP_SECRET'

USER_ID = 'USER_ID'

USER_TOKEN= 'USER_TOKEN'
FB_TOKEN = 'FB_TOKEN'

# Facebook Graph API
graph = facebook.GraphAPI(access_token=FB_TOKEN, version='2.2')
```

If necessary, a user can conveniently request to extend their access token through the API:
```python
graph.extend_access_token(FB_APP_ID, FB_APP_SECRET)
```

