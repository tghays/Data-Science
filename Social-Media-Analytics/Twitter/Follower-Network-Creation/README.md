# Follower Network Creation

This script uses Selenium to scrape Twitter and retrieve a handle's followers, then the followers of followers, and so on, to create a network web of integrated followers.


## How it works

Specify the path to the web driver for firefox.  Web Drivers must be downloaded and referenced for python web scraping, unless a headless browser is used, as with [PhantomJS](http://phantomjs.org/).
```python
gecko_path = '/Users/thays/anaconda/envs/python2.7/lib/python2.7/site-packages/selenium'
```

Define the scrolling function.  This function handles the scrolling action of the web driver.  This function scrolls to the end of the page waiting for changes in page loading. A simple sleep (wait) function is used to wait for the page to load, which is variable based on connection speed. A more efficient approach would be to check if the loading gif image element was present in the page, and adjust functionality accordingly.
```python
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
```

Get a list of the first-level followers for UNC_Basketball, initially acquired using Tweepy. A test list is used in this example.
```python
sm_follower_ids_df = pd.DataFrame.from_csv('/Users/thays/Desktop/twitter_influencer_search_engine/sm_followers.csv')
sm_followers_ids = list(sm_follower_ids_df['follower'])
main_df = pd.DataFrame(columns = ['user', 'follower'])
sm_followers_ids_test = sm_followers_ids[:10]
```

Iterate through the first-level followers and open their twitter page, then scrape through the page retrieving follower links.  Append the follower's of the first-level follower to a list, then append to a Pandas DataFrame.
```python
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
```
