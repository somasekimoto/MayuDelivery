# -*- coding:utf-8 -*-
import logging
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import TextSendMessage

import requests
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# 画像をスクレイピングするメソッド
def get_images(event, context):

    return{"status_code": 200, "body": "get_images successfully executed"}


# メッセージを受けて、返信するメソッド
def linebot(oevent, context):
    # リクエスト本体と、X-LINE-Signatureヘッダを取出す
    logger.info(f"Get message: {oevent}")
    body = oevent['body']
    signature = oevent['headers']['X-Line-Signature']

    # Channel Secretを使って入力が正しいかを確認する
    secret = os.getenv('LINE_CHANNEL_SECRET')

    parser = WebhookParser(secret)
    logger.info("Authentication OK.")

    # LineBotAPIオブジェクトを作成する
    token = os.getenv('LINE_ACCESS_TOKEN')

    line_bot_api = LineBotApi(token)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return {"stautsCode": 400, "body": ""}

    for event in events:
        logger.info(event)
        if event.type == 'message':
            reply_token = event.reply_token
            try:
                msg = event.message.text

                line_bot_api.reply_message(
                    reply_token, TextSendMessage(text=msg))
            except LineBotApiError as e:
                print(e.status_code)
                print(e.error.message)
                print(e.error.details)

    return {"stautsCode": 200, "body": "OK"}
