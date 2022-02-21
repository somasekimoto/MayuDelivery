import os
import tweepy
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import re
from linebot.models import (
    BubbleContainer, BoxComponent, TextComponent,
    FlexSendMessage, ImageComponent, URIAction, IconComponent, CarouselContainer, ButtonComponent
)
import pytz

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
jptz = pytz.timezone('Asia/Tokyo')


def create_contents(tweets):
    contents = []
    hour_ago = jptz.localize(datetime.now() - timedelta(hours=1, minutes=1))
    for t in tweets:
        created_at = t.created_at + timedelta(hours=9)
        if created_at > hour_ago:
            print(t.full_text)
            print(t.created_at)
            profile_image = t.user.profile_image_url_https
            text = t.full_text
            is_retweeted = re.match('^RT', text)
            header_text = '公式のツイート' if not is_retweeted else '公式のリツイート'
            main_color = '#08B901' if is_retweeted else '#1EA2F1'
            tweeter = t.retweeted_status.user if is_retweeted else t.user
            tweeter_icon = tweeter.profile_image_url_https
            try:
                extended_entities = t.retweeted_status.extended_entities
                media = extended_entities['media'] if is_retweeted else t.media
                images = [
                    ImageComponent(
                        type="image",
                        url=m['media_url_https'],
                        aspect_ratio='1:1',
                        aspect_mode='cover',
                        margin="md",
                    )
                    for m in media
                ]
            except:
                images = []
            contents.append(
                {
                    'header_text': header_text,
                    'main_color': main_color,
                    'text': text,
                    'profile_image': profile_image.replace('_normal', ''),
                    'tweeter_icon': tweeter_icon.replace('_normal', ''),
                    'tweet_url': 'https://twitter.com/hiratahirata14/status/' + t.id_str,
                    'images': images,
                }
            )
            print('---------------')
        else:
            print('---------------')
    return contents


def create_bubble_messages(contents):
    bubble_messages = []
    for o in contents:
        header_text = o['header_text']
        header = BoxComponent(
            type="box",
            layout="vertical",
            background_color=o['main_color'],
            contents=[
                TextComponent(
                    type="text",
                    text=header_text,
                    weight="bold",
                    color="#FFFFFF",
                )
            ]
        )
        hero = ImageComponent(
            url=o['profile_image'],
            size='full',
            aspect_ratio='2:1',
            aspect_mode='cover',
            action=URIAction(uri=o['tweet_url'])
        )
        body_image_box = BoxComponent(
            type="box",
            layout='horizontal',
            contents=o['images'],
        )
        body_text_box = BoxComponent(
            type="box",
            layout='baseline',
            contents=[
                IconComponent(
                    type="icon",
                    url=o['tweeter_icon'],
                    size="sm",
                    aspect_ratio="1:1",
                ),
                TextComponent(
                    type="text",
                    text=o['text'],
                    weight='bold',
                    size='sm',
                    wrap=True,
                ),
            ],
        )
        body = BoxComponent(
            type="box",
            layout='vertical',
            contents=[
                body_image_box,
                body_text_box,
            ],
        )
        footer_button = ButtonComponent(
            type="button",
            style="primary",
            action=URIAction(uri=o['tweet_url'], label='このツイートを見る'),
            color=o['main_color'],
        )
        footer = BoxComponent(
            type="box",
            layout="horizontal",
            contents=[
                footer_button,
            ],
        )
        bubble = BubbleContainer(
            type="bubble",
            direction='ltr',
            header=header,
            hero=hero,
            body=body,
            footer=footer,
        )
        bubble_messages.append(bubble)
    return bubble_messages


def check_official():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.user_timeline(
        screen_name='hiratahirata14', count=10, exclude_replies=True,
        tweet_mode="extended", include_entities=True
    )

    contents = create_contents(tweets)

    if not contents:
        return []
    print(contents)

    bubble_messages = create_bubble_messages(contents)

    carousel = CarouselContainer(
        type="carousel",
        contents=bubble_messages,
    )
    message = FlexSendMessage(alt_text="松岡茉優 公式ツイート", contents=carousel)
    return [message]


if __name__ == "__main__":
    check_official()
