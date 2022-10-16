from logic import get_tweets, get_reddits, reddits_to_df, tweets_to_df


def test_reddit():
    # feeds = ["hot", "new", "top"]
    feed = "hot"
    subreddits = ["news", "worldnews"]
    reddits = []
    for subr in subreddits:
        reddits += get_reddits(subr, feed, 100)
    reddits_to_df(reddits)


def test_twitre():
    accounts = ["BBCBreaking", "washingtonpost", "cnnbrk"]
    tweets = []
    for acc in accounts:
        tweets += get_tweets(acc, 100)
    tweets_to_df(tweets)
