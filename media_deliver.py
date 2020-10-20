# -*- coding:utf-8 -*-
import logging
import os
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

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
        function_name = context.function_name.split('-')[-1]
        messages = getattr(eval(function_name), function_name)()
        print('messages')
        print(messages)

        if os.getenv('STAGE') == 'prod':
            for message in messages:
                line_bot_api.broadcast(
                    message
                )
        else:
            user_id = os.getenv('USER_ID')
            for message in messages:
                line_bot_api.push_message(
                    user_id,
                    message
                )

    except LineBotApiError as e:
        print(e.status_code)
        print(e.error.message)
        print(e.error.details)

    return {"stautsCode": 200, "body": "OK"}


if __name__ == '__main__':
    send_media(None, None)
