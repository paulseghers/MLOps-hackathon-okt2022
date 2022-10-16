from logic import get_reddits, reddits_to_df, get_tweets, tweets_to_df
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("output", type=click.File("wb"))
@click.argument("subreddits", nargs=-1)
@click.option("--feed", default="hot")
@click.option("--limit", type=int, default=100)
def reddit(output, subreddits, feed, limit):
    reddits = []
    for subr in subreddits:
        reddits += get_reddits(subr, feed, limit)
    df = reddits_to_df(reddits)
    df.to_csv(output)


@cli.command()
@click.argument("output", type=click.File("wb"))
@click.argument("accounts", nargs=-1)
@click.option("--limit", type=int, default=100)
def twitter(output, accounts, limit):
    tweets = []
    for acc in accounts:
        tweets += get_tweets(acc, limit)
    df = tweets_to_df(tweets)
    df.to_csv(output, index=False)


if __name__ == "__main__":
    cli()
