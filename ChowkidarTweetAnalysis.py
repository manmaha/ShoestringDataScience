#!/usr/bin/env python
# coding: utf-8

# # Data Science on a ShoeString - 1
# Manish Mahajan 8 May 2019
# # Simple Data Analysis using Twitter

# ## Set up Twitter for Python



import tweepy # the twitter library we shall be using
import sys
import pandas as pd

# These API keys are obtained when you register your Twitter account as a developer
# you need to obtain the authorisation and then paste these keys here

apiKey = 'Replace with your key'
apiSecret = 'Replace with your Secret'
accessToken = 'Replace with your access token'
accessTokenSecret = 'Replace with your Secret'

apiKey = 'JWgKfdS1A5P9oHKlab5tqItlP'
apiSecret = 'ucC9Nh4pMDUAACt77bW8pUF11OexcoOvQpSUdroPmo7KoXxCgh'
accessToken = '940940585434677253-xfvgSfbFGhSEBx94F8zJs7pbMd3VLBW'
accessTokenSecret = 'RcFS69zjoDMs5N2b7LG3fdHBuSfibVQSvuPaVAg2396t5'


# Authorise Tweepy to use your keys

auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)


# ## Kitne Chowkidar Hain
#
# Get a list of active chowkidars from Twitter
#
# The Twitter api does not allow us to retrieve more than 1020 (20 users per page and 51 pages in total)

# In[2]:


query = '"chowkidar"'
chowkidars =[]
for page in range(1,52):
    chowkidars+=api.search_users(query,20,page)


# ### Collect their last 20 tweets

# In[ ]:





# In[11]:


tweets = []
for steps in range(0,1000,100):
    for user in chowkidars[steps:steps+100]:
        try:
            tweets+= [t.text for t in  api.user_timeline(user.id)]
        except:
            pass
for user in chowkidars[1000:len(chowkidars)]:
        try:
            tweets+= [t.text for t in  api.user_timeline(user.id)]
        except:
            pass


# In[46]:


total_chowkidars = len(chowkidars)
total_tweets = len(tweets)


# In[80]:


import pandas as pd
df = pd.DataFrame(tweets, columns=['text'])
nehruvianQuery = 'Nehru|Rajiv|Jwahar[lal]| Jawahr[lal]|Indira|Jawahar[lal]|Bofors|Bofars|जवाहरलाल|नेहरु|राजीव|इन्दिरा|इन्दीरा'
nehruvianTweets = df['text'].str.contains(nehruvianQuery,case=False, regex=True).value_counts()

#lets check the number of Devnagri Tweets, query2 is the unicode list of the devnagri language
devnagriQuery = '[\u0900-\u097F]'
devnagri= df['text'].str.contains(devnagriQuery,case=False, regex=True).value_counts()

#Lets do some reporting
print("I was able to extract {:d} Chowkidars most active on Twitter in the last few days\n".format(total_chowkidars))
print("Top 10 Twitter Handles are:\n")
for user in chowkidars[0:10]:
      print(user.screen_name)
print("\n{:.2f}% of {:d} Chowkidar Tweets extracted are in Devnagri".format(devnagri[1]/total_tweets*100,total_tweets))
print("\nI queried for Tweets containing Nehru,Indira,Rajiv,Jawaharlal and Bofors\n")
print("\n{:.2f}% of {:d} Chowkidar Tweets refer to dead Nehru-Gandhis".format(nehruvianTweets[1]/total_tweets*100,total_tweets))


# In[81]:


#Lets check if we're picking up the right devnagri tweets, first time working with devnagri text
devnagriNehruQuery = 'जवाहरलाल|नेहरु|राजीव|इन्दिरा|इन्दीरा'
devnagriNehruvianTweets = df['text'].str.contains(devnagriNehruQuery,case=False, regex=True).value_counts()
d = df['text'].str.contains(query,case=False, regex=True)
df['text'][d==True]
