"""Main file to run topic analysis"""


import logging
import pickle as pkl

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

from gensim import corpora, models, similarities
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def load_tweets(pklfile=None):
    """load the dictionary of tweets from the pickle file;
    in the form:
    [tweet_id]: "tweet text" """

    with open(pklfile, 'r') as pfile:
        tweet_file = pkl.load(pfile)
        return tweet_file


def remove_screen_name(tweet):
    """For a given tweet, remove the screen name (e.g. @LastWeekTonight) and
    return the tweet"""

    new_tweet = []
    words = tweet.split()
    for word in words:
        if 'http' not in word and '@' not in word:
            new_tweet.append(word)

    return ' '.join(new_tweet)


def nopunkt_tokenize(sentence='a b c'):
    """tokenize a string, by removing also punctuation"""

    punctuation = [char for char in string.punctuation]
    stops = stopwords.words('english')
    stops.extend(punctuation)
    stops.extend(["\'s", "'", '"', '``', "''"])
    tokens = [token for token in word_tokenize(sentence.lower())
              if token not in stops]

    return tokens


def dict_to_list(tweets_dict):
    """Return the corpus of documents in list format, from the dictionary
    of tweets"""

    documents = [remove_screen_name(tweet)
                 for tweet in tweets_dict.itervalues()
                 if not tweet.startswith('RT')]

    return documents


if __name__ == '__main__':
    tweets_dict = load_tweets('LastWeekTonight_tweets.pkl')
    documents = dict_to_list(tweets_dict)

    # list of lists of words
    texts = [nopunkt_tokenize(sent) for sent in documents]

    # dictionary of tokens to ids
    dictionary = corpora.Dictionary(texts)

    # corpus in bag-of-words space
    corpus = [dictionary.doc2bow(text) for text in texts]

























