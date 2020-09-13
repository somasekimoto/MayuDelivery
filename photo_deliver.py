# -*- coding:utf-8 -*-
import logging
from linebot import LineBotApi

from linebot.exceptions import LineBotApiError
from linebot.models import (
    TextSendMessage, ImageSendMessage,
)

import requests
import os
import time

import search_tweets

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_photos(event, context):

    logger.info("Authentication OK.")
    # LineBotAPIオブジェクトを作成する
    token = os.getenv('LINE_ACCESS_TOKEN')

    line_bot_api = LineBotApi(token)

    try:
        all_img_src_list = search_tweets.search_photos()
        print('all_img_src_list')
        print(all_img_src_list)

        image_messages = []

        for src in all_img_src_list:
            item = ImageSendMessage(
                original_content_url=src, preview_image_url=src)
            image_messages.append(item)

        print('image_messages')
        print(image_messages)
        if os.getenv('STAGE') == 'prod':
            line_bot_api.broadcast(
                image_messages[0:3]
            )
            line_bot_api.broadcast(
                image_messages[4:8]
            )
        else:
            user_id = os.getenv('USER_ID')
            line_bot_api.push_message(
                user_id,
                image_messages[0:3]
            )
            line_bot_api.push_message(
                user_id,
                image_messages[4:8]
            )

    except LineBotApiError as e:
        print(e.status_code)
        print(e.error.message)
        print(e.error.details)

    return {"stautsCode": 200, "body": "OK"}


if __name__ == '__main__':
    send_photos(None, None)
