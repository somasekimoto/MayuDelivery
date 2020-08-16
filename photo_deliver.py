# -*- coding:utf-8 -*-
import logging
from linebot import LineBotApi

from linebot.exceptions import LineBotApiError
from linebot.models import (
    TextSendMessage, ImageSendMessage,
)

import requests
import os
import json
from bs4 import BeautifulSoup
import urllib.request
import time


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
    img_num_per_page = 1
    page_list = [f'{url}{i*img_num_per_page+1}' for i in range(max_page_num)]
    return page_list


def send_photos(event, context):

    logger.info("Authentication OK.")
    # LineBotAPIオブジェクトを作成する
    token = os.getenv('LINE_ACCESS_TOKEN')

    line_bot_api = LineBotApi(token)

    try:
        url = "https://www.google.com/search?q=%E6%9D%BE%E5%B2%A1%E8%8C%89%E5%84%AA&tbm=isch&hl=ja&hl=ja&tbs=qdr%3Aw&ved=0CAMQpwVqFwoTCLDl0b-b2OoCFQAAAAAdAAAAABAC&biw=1440&bih=740"
        MAX_PAGE_NUM = 1
        all_img_src_list = scraping(url, MAX_PAGE_NUM)
        print('all_img_src_list')
        print(all_img_src_list)

        array = []

        for src in all_img_src_list:
            item = ImageSendMessage(
                original_content_url=src, preview_image_url=src)
            array.append(item)

        print('array')
        print(array)
        if os.getenv('STAGE') == 'prod':
            line_bot_api.broadcast(
                array[0:4]
            )
        else:
            user_id = os.getenv('USER_ID')
            line_bot_api.push_message(
                user_id,
                array[0:4]
            )

    except LineBotApiError as e:
        print(e.status_code)
        print(e.error.message)
        print(e.error.details)

    return {"stautsCode": 200, "body": "OK"}


if __name__ == '__main__':

    send_photos(None, None)
