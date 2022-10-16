from typing import List
from pydantic import BaseModel
from fastapi import FastAPI

from logic import get_reddits, reddits_to_df, get_tweets, tweets_to_df


app = FastAPI()


class RedditRequest(BaseModel):
    subreddits: List[str]
    feed: str = "hot"
    limit: int = 100
    dest: str


@app.post("/reddit")
def api_reddit(req: RedditRequest):
    try:
        reddits = []
        for subr in req.subreddits:
            reddits += get_reddits(subr, req.feed, req.limit)
        df = reddits_to_df(reddits)
        df.to_gbq(req.dest)
    except Exception as e:
        return repr(e)
    return "OK"


class TwitterRequest(BaseModel):
    accounts: List[str]
    limit: int = 100
    dest: str


@app.post("/twitter")
def api_twitter(req: TwitterRequest):
    try:
        tweets = []
        for acc in req.accounts:
            tweets += get_tweets(acc, req.limit)
        df = tweets_to_df(tweets)
        df.to_gbq(req.dest)
    except Exception as e:
        return repr(e)
    return "OK"
