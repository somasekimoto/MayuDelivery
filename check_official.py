import os
import tweepy
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import re
import logging
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import (
    BubbleContainer, BoxComponent, TextComponent,
    FlexSendMessage, ImageComponent, URIAction
)

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_official(event, context):
    logger.info("Authentication OK.")
    # LineBotAPIオブジェクトを作成する
    token = os.getenv('LINE_ACCESS_TOKEN')
    line_bot_api = LineBotApi(token)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name='hiratahirata14')
    official_tweets = []
    for t in tweets:
        if not re.match('^RT', t.text) and t.created_at >= datetime.now() - timedelta(hours=1, minutes=1):
            print(datetime.now())
            print(t.text)
        else:
            print(t.user.profile_image_url_https)
            official_tweets.append(
                {
                    'text': t.text,
                    'profile_image': t.user.profile_image_url_https.replace('_normal', ''),
                    'tweet_url': 'https://twitter.com/hiratahirata14/status/' + t.id_str,
                }
            )
            print('---------------')

    # print(official_tweets)
    profile_image = api.get_user(screen_name='hiratahirata14')
    print(profile_image)
    # for o in official_tweets:
    bubble = BubbleContainer(
        type="bubble",
        direction='ltr',
        hero=ImageComponent(
            url=official_tweets[0]['profile_image'],
            size='full',
            aspect_ratio='10:10',
            aspect_mode='cover',
            action=URIAction(
                  uri=official_tweets[0]['tweet_url'], label='label')
        ),
        body=BoxComponent(
            type="box",
            layout='vertical',
            contents=[
                # title
                TextComponent(
                    type="text",
                    text=official_tweets[0]['text'],
                    weight='bold',
                    size='sm',
                ),
            ]
        ),
    )
    message = FlexSendMessage(alt_text="オフィシャルのお知らせ", contents=bubble)
    user_id = os.getenv('USER_ID')
    line_bot_api.push_message(
        user_id,
        message
    )


if __name__ == "__main__":
    check_official()
