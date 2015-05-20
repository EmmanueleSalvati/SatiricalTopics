# SatiricalTopics
Topic modeling of tweets by J. Oliver, J. Stewart, S. Colbert, and B. O'Reilly

Unfortunately, Twitter only allows up to 3200 tweets to be retrieved. My project hit a dead-end, because it is not enough to take into account of the variation of topics in the tweets.

## Useful functions
    import API_clustering as api
    tweets = api.tweets(oauth, max_id, screen_name='someusername')

    status = api.api_status(oauth)