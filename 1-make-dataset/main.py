from typing import List
from pydantic import BaseModel
import functions_framework

from logic import get_reddits, reddits_to_df, get_tweets, tweets_to_df


class RedditRequest(BaseModel):
    subreddits: List[str]
    feed: str = "hot"
    limit: int = 100
    dest: str


def api_reddit(req: RedditRequest):
    reddits = []
    for subr in req.subreddits:
        reddits += get_reddits(subr, req.feed, req.limit)
    df = reddits_to_df(reddits)
    df.to_gbq(req.dest)


class TwitterRequest(BaseModel):
    accounts: List[str]
    limit: int = 100
    dest: str


def api_twitter(req: TwitterRequest):
    tweets = []
    for acc in req.accounts:
        tweets += get_tweets(acc, req.limit)
    df = tweets_to_df(tweets)
    df.to_gbq(req.dest)


@functions_framework.http
def entrypoint(request):
    payload = request.get_json()
    func, cls = {
        "reddit": (api_reddit, RedditRequest),
        "twitter": (api_twitter, TwitterRequest),
    }[payload.pop("source")]
    # execute
    func(cls(**payload))
