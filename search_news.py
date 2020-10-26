import os
import tweepy
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json

from linebot.models import (
    BubbleContainer, BoxComponent, TextComponent,
    FlexSendMessage, ImageComponent, URIAction, IconComponent, CarouselContainer, ButtonComponent
)

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


def layout_message(news_tweets):
    contents = []
    for tweet in news_tweets:
        print(tweet.user.name)
        print(tweet.full_text)
        print(tweet.favorite_count)
        print(tweet.entities['urls'][0]['expanded_url'])
        contents.append(
            {
                'user_name': tweet.user.name,
                'text': tweet.full_text,
                'favorite_count': tweet.favorite_count,
                'news_url': tweet.entities['urls'][0]['expanded_url'],
            }
        )
        print("------------------------------------------------------------")

    unique_contents = list(map(json.loads, set(map(json.dumps, contents))))
    sorted_contents = sorted(
        unique_contents,
        key=lambda x: x['favorite_count'],
        reverse=True
    )
    print(sorted_contents)
    # return False
    # header_text = o['header_text']
    # header = BoxComponent(
    #     type="box",
    #     layout="vertical",
    #     contents=[
    #         TextComponent(
    #             type="text",
    #             text=tweet,
    #             weight="bold",
    #         )
    #     ]
    # )
    # hero = ImageComponent(
    #     url=o['profile_image'],
    #     size='full',
    #     aspect_ratio='2:1',
    #     aspect_mode='cover',
    #     action=URIAction(uri=o['tweet_url'])
    # )
    # body_image_box = BoxComponent(
    #     type="box",
    #     layout='horizontal',
    #     contents=o['images'],
    # )
    # body_text_box = BoxComponent(
    #     type="box",
    #     layout='baseline',
    #     contents=[
    #         IconComponent(
    #             type="icon",
    #             url=o['tweeter_icon'],
    #             size="sm",
    #             aspect_ratio="1:1",
    #         ),
    #         TextComponent(
    #             type="text",
    #             text=o['text'],
    #             weight='bold',
    #             size='sm',
    #             wrap=True,
    #         ),
    #     ],
    # )
    # body = BoxComponent(
    #     type="box",
    #     layout='vertical',
    #     contents=[
    #         body_image_box,
    #         body_text_box,
    #     ],
    # )
    # footer_button = ButtonComponent(
    #     type="button",
    #     style="primary",
    #     action=URIAction(uri=o['tweet_url'], label='このツイートを見る'),
    #     color="#1EA2F1",
    # )
    # footer = BoxComponent(
    #     type="box",
    #     layout="horizontal",
    #     contents=[
    #         footer_button,
    #     ],
    # )
    # bubble = BubbleContainer(
    #     type="bubble",
    #     direction='ltr',
    #     header=header,
    #     hero=hero,
    #     body=body,
    #     footer=footer,
    # )
    # official_contents.append(bubble)


def search_news(event, context):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    yesterday = datetime.strftime(
        datetime.today() - relativedelta(days=1), f"%Y-%m-%d")

    # q = f"#松岡茉優 OR 松岡茉優 filter:news exclude:retweets filter:verified since:{yesterday}"
    q = f"#松岡茉優 OR 松岡茉優 filter:news exclude:retweets filter:verified"

    news_tweets = tweepy.Cursor(
        api.search,
        q=q,
        tweet_mode='extended',
        include_entities=True,
        result_type='mixed',
        count=20,
    ).items(20)

    messages = layout_message(news_tweets)


if __name__ == "__main__":
    search_news()
