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

Prepare Pandas DataFrame with relevant columns:
```python
fb_comments_df = pd.DataFrame(columns = ['reply_comment_date', 'reply_comment_time', 'reply_comment_text', \
                                          'reply_comment_id', 'reply_username', 'reply_user_id', 'brand', 'post_date',\
                                          'post_time', 'post_text', 'post_id'])
```

Get posts from the RDU user, appends them to "temp_posts" list.  Then itereate through each post, then further iterate through the comments of each post.
```python
brand_id = '145265145503493'
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

temp_fb_comments_df = pd.DataFrame(columns = ['reply_comment_date', 'reply_comment_time', 'reply_comment_text', \
                                      'reply_comment_id', 'reply_username', 'reply_user_id', 'brand', 'post_date',\
                                      'post_time', 'post_text', 'post_id'])

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

    temp_df = pd.DataFrame(columns = ['reply_comment_date', 'reply_comment_time', 'reply_comment_text', \
                                      'reply_comment_id', 'reply_username', 'reply_user_id', 'brand', 'post_date',\
                                      'post_time', 'post_text', 'post_id'])

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
```
