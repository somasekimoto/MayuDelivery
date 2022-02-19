import os
import tweepy
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json
import requests
from bs4 import BeautifulSoup
import lxml
from linebot.models import (
    FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, SeparatorComponent, URIAction
)
import html5lib


consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


def create_contents(news_tweets):
    contents = []
    for tweet in news_tweets:
        response = requests.get(tweet.entities['urls'][0]['expanded_url'])
        # soup = BeautifulSoup(response.text, "lxml")
        soup = BeautifulSoup(response.text, "html5lib")
        if soup.title is None:
            news_title = "タイトルが取得できませんでした"
        else:
            news_title = soup.title.string
        news_url = tweet.entities['urls'][0]['expanded_url']
        contents.append(
            {
                'title': news_title,
                'favorite_count': tweet.favorite_count,
                'news_url': news_url,
            }
        )
        print("------------------------------------------------------------")
    if not contents:
        return []
    print(contents)

    sorted_contents = sorted(
        contents,
        key=lambda x: x['favorite_count'],
        reverse=True,
    )

    titles = []
    unique_contents = []
    for c in sorted_contents:
        if c['title'] not in titles:
            titles.append(c['title'])
            unique_contents.append(c)
    print(unique_contents)
    return unique_contents[0:5]


def design_message(contents):
    body_comps = []
    for t in contents:
        header_text = TextComponent(
            type="text",
            text=t['title'],
            weight='bold',
            size='xs',
            margin='md',
            gravity='center',
            wrap=True,
            action=URIAction(uri=t['news_url']),
        )

        box = BoxComponent(
            type='box',
            layout='vertical',
            contents=[
                header_text,
                SeparatorComponent(
                    type='separator',
                ),
            ]
        )
        body_comps.append(box)

    header = BoxComponent(
        type="box",
        layout="vertical",
        background_color="#F06161FF",
        contents=[
            TextComponent(
                type="text",
                text="〜 まゆニュース 〜",
                weight="bold",
                color="#FFFFFFFF",
            )
        ]
    )
    body_text_box = BoxComponent(
        type="box",
        layout='vertical',
        contents=body_comps,
    )
    body = BoxComponent(
        type="box",
        layout='vertical',
        contents=[
            body_text_box,
        ],
    )
    footer = BoxComponent(
        type="box",
        layout="vertical",
        background_color="#F06161FF",
    )
    bubble = BubbleContainer(
        type="bubble",
        direction='ltr',
        header=header,
        body=body,
        footer=footer,
    )
    message = FlexSendMessage(alt_text="まゆニュース", contents=bubble)
    return [message]


def search_news():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    now = datetime.utcnow()
    twelve_hours = relativedelta(hours=12, minutes=1)
    half_day = datetime.strftime(now - twelve_hours, f"%Y-%m-%d_%H:%M:%S")

    q = f"#松岡茉優 OR 松岡茉優 filter:news exclude:retweets since:{half_day}"

    news_tweets = tweepy.Cursor(
        api.search_tweets,
        q=q,
        tweet_mode='extended',
        include_entities=True,
        result_type='mixed',
        count=30
    ).items()

    contents = create_contents(news_tweets)
    if not contents:
        return []
    return design_message(contents)


if __name__ == "__main__":
    search_news()
