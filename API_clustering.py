"""Twitter API"""

import requests
from requests_oauthlib import OAuth1
import os.path
import pickle as pkl
import Twitter_keys as tks


def oauth():
    """get the OAuth1 object"""

    consumer_key = tks.consumer_key
    consumer_secret = tks.consumer_secret
    access_token = tks.access_token
    access_secret = tks.access_secret

    return OAuth1(consumer_key,
                  client_secret=consumer_secret,
                  resource_owner_key=access_token,
                  resource_owner_secret=access_secret)


def get_pkl_dict(dict_file):
    with open(dict_file, 'r') as pklfile:
        pkl_dict = pkl.load(pklfile)

    return pkl_dict


def tweets(oauth, max_id=None, count=200, screen_name='LastWeekTonight'):
    """Make the call to Twitter and return a dict of tweets"""

    search_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    parameters = {'count': count, 'screen_name': screen_name}
    if max_id:
        parameters['max_id'] = max_id
    response = requests.get(search_url, auth=oauth, params=parameters)
    tweets = response.json()

    return tweets


def get_max_id(text_file=None):
    """Read max_id from max_id text file"""

    max_id = None
    if text_file:
        with open(text_file) as f:
            max_id = f.read()
    return max_id


def remove_screen_name(tweet):
    """For a given tweet, remove the screen name (e.g. @LastWeekTonight) and
    return the tweet"""

    new_tweet = []
    words = tweet.split()
    for word in words:
        if 'http' not in word and '@' not in word:
            new_tweet.append(word)

    return ' '.join(new_tweet)


# def calc_min_distance(cluster, centroid):
#     """For every tweet in the cluster, calculate the minimum distance between
#     a tweet and the centroid"""

#     distances = []
#     for tweet in cluster:


if __name__ == '__main__':
    max_id = None
    if os.path.exists("max_id.txt"):
        max_id = get_max_id('max_id.txt')

    oauth = oauth()
    tweets = tweets(max_id)

    LastWeekTonight = {}
    if os.path.exists('LastWeekTonight_tweets.pkl'):
        LastWeekTonight = get_pkl_dict('LastWeekTonight_tweets.pkl')

    for tweet in tweets:
        LastWeekTonight[tweet['id']] = tweet['text']

    with open('max_id.txt', 'w') as max_text:
        max_text.write(str(tweets[-1]['id']))

    with open('LastWeekTonight_tweets.pkl', 'w') as pklfile:
        pkl.dump(LastWeekTonight, pklfile)
