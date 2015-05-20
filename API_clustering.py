"""Twitter API"""

import requests
from requests_oauthlib import OAuth1
import os.path
import pickle as pkl
import Twitter_keys as tks
import argparse

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


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


def api_status(oauth):
    """Make a call to Twitter to see the status of my rate limitations"""

    search_url = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
    parameters = {'resources': 'statuses'}
    response = requests.get(search_url, auth=oauth, params=parameters)
    status = response.json()

    return status


def tweets(oauth, max_id=None, count=200, screen_name='LastWeekTonight'):
    """Make the call to Twitter and return a dict of tweets"""

    search_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    parameters = {'count': count, 'screen_name': screen_name,
                  'exclude_replies': 'true'}
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


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Twitter username, without @")
    args = parser.parse_args()

    username = args.username

    max_id = None
    if os.path.exists("%s_max_id.txt" % username):
        max_id = get_max_id('%s_max_id.txt' % username)

    oauth = oauth()

    # Returns the status of your requests, i.e. how many calls you have left
    status = api_status(oauth)

    tweets = tweets(oauth, max_id, screen_name=username)

    tweets_tosave = {}
    if os.path.exists('%s_tweets.pkl' % username):
        tweets_tosave = get_pkl_dict('%s_tweets.pkl' % username)

    for tweet in tweets:
        tweets_tosave[tweet['id']] = [tweet['text'], tweet['created_at']]

    with open('%s_max_id.txt' % username, 'w') as max_text:
        max_text.write(str(tweets[-1]['id']))

    with open('%s_tweets.pkl' % username, 'w') as pklfile:
        pkl.dump(tweets_tosave, pklfile)
