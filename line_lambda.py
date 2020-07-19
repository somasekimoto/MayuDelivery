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
from bs4 import BeautifulSoup
import urllib.request
import time
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# 画像をスクレイピングするメソッド
def scraping(url, max_page_num):
    # ページネーション実装
    page_list = get_page_list(url, max_page_num)
    # 画像URLリスト取得
    all_img_src_list = []
    for page in page_list:
        img_src_list = get_img_src_list(page)
        all_img_src_list.extend(img_src_list)
    return all_img_src_list


def get_img_src_list(url):
    # 検索結果ページにアクセス
    response = requests.get(url)
    # レスポンスをパース
    soup = BeautifulSoup(response.text, 'html.parser')
    img_src_list = [img.get('src') for img in soup.select('td img')]
    return img_src_list


def get_page_list(url, max_page_num):
    img_num_per_page = 20
    page_list = [f'{url}{i*img_num_per_page+1}' for i in range(max_page_num)]
    return page_list


def download_img(src, dist_path):
    time.sleep(1)
    try:
        bucket = 'image-catcher-dev-asset'
        s3 = boto3.resource('s3')
        with urllib.request.urlopen(src) as data:
            img = data.read()
            with open(dist_path, 'wb') as f:
                f.write(img)
                s3.Bucket(bucket).put_object(Key=dist_path, Body=img)
    except:
        return {"errorMessage": "download error"}


def main(event, context):
    url = "https://www.google.com/search?q=%E6%9D%BE%E5%B2%A1%E8%8C%89%E5%84%AA&tbm=isch&hl=ja&hl=ja&tbs=qdr%3Aw&ved=0CAMQpwVqFwoTCLDl0b-b2OoCFQAAAAAdAAAAABAC&biw=1440&bih=740"
    MAX_PAGE_NUM = 1
    all_img_src_list = scraping(url, MAX_PAGE_NUM)
    # 画像ダウンロード
    for i, src in enumerate(all_img_src_list):
        download_img(src, f'/tmp/mayu_{i + 1}.jpg')


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


if __name__ == '__main__':
    main(None, None)
