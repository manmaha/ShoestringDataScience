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



tweets = []
for user in chowkidars:
        try:
            tweets+= [t.text for t in  api.user_timeline(user.id)]
        except:
            pass


total_chowkidars = len(chowkidars)
total_tweets = len(tweets)

import pandas as pd
df = pd.DataFrame(tweets, columns=['text'])

#Build up queries
nehru = 'Nehru|Jwahar(lal)?| Jawahr(lal)?|Jawahar(lal)?|जवाहरलाल|जवाहर(लाल)?|नेहरु'
indira = 'Indira|इन्दिरा|इन्दीरा'
rajiv = 'Rajiv|Bofors|Bofars|राजीव|बोफोर्स|बोफर्स'
others = ''


religious_query = religious_query = 'Hindu(s)?($|\b)|Hinduism|Hindutv|Muslim(s)?|Moslem(s)?|Islam|Muss?alman(s)|Mohammaden(s)?|मुस्लिम|इस्लाम|मुस्सलमान|मुस्लमान'


nehruvian_query = nehru+'|'+indira+'|'+rajiv
nehruvian_tweets = df['text'].str.contains(nehruvian_query,case=False, regex=True).value_counts()
religious_query = 'Hindu(s)?($|\b)|Hinduism|Hindutv|Dharm(a)?|Muslim(s)?|Moslem(s)?|Islam|Muss?alman(s)|Mohammaden(s)?|धर्म|मुस्लिम|इस्लाम|मुस्सलमान|मुस्लमान'
religious_tweets = df['text'].str.contains(religious_query,case=False, regex=True).value_counts()

#lets check the number of Devnagri Tweets, query2 is the unicode list of the devnagri language
devnagri_query = '[\u0900-\u097F]'
devnagri= df['text'].str.contains(devnagri_query,case=False, regex=True).value_counts()

#Lets do some reporting
print("I was able to extract {:d} Chowkidars most active on Twitter in the last few days\n".format(total_chowkidars))
print("Top 10 Twitter Handles are:\n")
for user in chowkidars[0:10]:
      print(user.screen_name)
print("\n{:.2f}% of {:d} Chowkidar Tweets extracted are in Devnagri".format(devnagri[1]/total_tweets*100,total_tweets))
print("\nI queried for Tweets containing Nehru/Indira/Rajiv/Jawaharlal/Bofors")
print("{:.2f}% of {:d} Chowkidar Tweets refer to dead Nehru-Gandhis".format(nehruvian_tweets[1]/total_tweets*100,total_tweets))
print("\nI queried for Tweets containing Hindu/Hindutva/Hinduim/Islam/Muslim")
print("{:.2f}% of {:d} Chowkidar Tweets refer to religion".format(religious_tweets[1]/total_tweets*100,total_tweets))


#Lets check if we're picking up the right devnagri tweets, first time working with devnagri text
devnagriNehruQuery = 'जवाहरलाल|नेहरु|राजीव|इन्दिरा|इन्दीरा'
devnagriNehruvianTweets = df['text'].str.contains(devnagriNehruQuery,case=False, regex=True).value_counts()
d = df['text'].str.contains(query,case=False, regex=True)
df['text'][d==True]
