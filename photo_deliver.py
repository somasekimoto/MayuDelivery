# -*- coding:utf-8 -*-
import logging
from linebot import LineBotApi

from linebot.exceptions import LineBotApiError
from linebot.models import (
    TextSendMessage, ImageSendMessage, VideoSendMessage
)

import requests
import os


import search_tweets

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_media(event, context):

    logger.info("Authentication OK.")
    # LineBotAPIオブジェクトを作成する
    token = os.getenv('LINE_ACCESS_TOKEN')

    line_bot_api = LineBotApi(token)

    try:
        # twitter 検索で画像と動画の URL オブジェクトの配列を取得
        all_media_list = search_tweets.search_tweets()
        print('all_media_list')
        print(all_media_list)

        messages = []

        for media in all_media_list:
            item = VideoSendMessage(
                original_content_url=media['origin'], preview_image_url=media['preview']) if media['type'] == 'video' else ImageSendMessage(
                original_content_url=media['origin'], preview_image_url=media['preview'])

            messages.append(item)

        print('messages')
        print(messages)
        if os.getenv('STAGE') == 'prod':
            line_bot_api.broadcast(
                messages[0:3]
            )
            line_bot_api.broadcast(
                messages[4:8]
            )
        else:
            user_id = os.getenv('USER_ID')
            line_bot_api.push_message(
                user_id,
                messages[0:3]
            )
            line_bot_api.push_message(
                user_id,
                messages[4:8]
            )

    except LineBotApiError as e:
        print(e.status_code)
        print(e.error.message)
        print(e.error.details)

    return {"stautsCode": 200, "body": "OK"}


if __name__ == '__main__':
    send_media(None, None)
