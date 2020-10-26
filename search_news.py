import os
import tweepy
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from linebot.models import (
    BubbleContainer, BoxComponent, TextComponent,
    FlexSendMessage, ImageComponent, URIAction, IconComponent, CarouselContainer, ButtonComponent
)

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


def search_news(event, context):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    yesterday = datetime.strftime(
        datetime.today() - relativedelta(days=1), f"%Y-%m-%d")

    q = f"#松岡茉優 OR 松岡茉優 filter:news exclude:retweets since:{yesterday}"
    # q = f"#松岡茉優 OR 松岡茉優 filter:news exclude:retweets"

    news_tweets = tweepy.Cursor(
        api.search,
        q=q,
        tweet_mode='extended',
        include_entities=True,
        result_type='mixed',
        count=20,
    ).items(20)

    news_contents = []
    for tweet in news_tweets:
        print(tweet)
        print("------------------------------------------------------------")


if __name__ == "__main__":
    search_news()
