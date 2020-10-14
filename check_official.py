import os
import tweepy
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import re

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


def check_official(event, context):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name='hiratahirata14')
    for t in tweets:
        if not re.match('^RT', t.text) and t.created_at >= datetime.now() - timedelta(hours=1, minutes=1):
            print(datetime.now())
            print(t.created_at)
        else:
            print(t.text)
            print('---------------')


if __name__ == "__main__":
    check_official()
