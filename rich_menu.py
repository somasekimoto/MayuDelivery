import os
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import (
    RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize, MessageAction, URIAction
)


def createRichmenu(event, context):
    # LineBotAPIオブジェクトを作成する
    token = os.getenv('LINE_ACCESS_TOKEN')
    line_bot_api = LineBotApi(token)

    result = False
    try:
        # define a new richmenu
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=2500, height=843),
            selected=False,
            name='richmenu for Link',
            chat_bar_text='MENU',
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=15, y=0, width=800, height=843),
                    action=URIAction(uri='https://www.matsuokamayu.jp/')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=845, y=0, width=800, height=843),
                    action=URIAction(uri='https://twitter.com/hiratahirata14/')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1660, y=0, width=800, height=843),
                    action=URIAction(
                        uri='https://www.instagram.com/mayu_matsuoka_koushiki/')
                )
            ]
        )
        richMenuId = line_bot_api.create_rich_menu(
            rich_menu=rich_menu_to_create)

        # upload an image for rich menu
        path = './images/rich_image.jpg'

        with open(path, 'rb') as f:
            line_bot_api.set_rich_menu_image(richMenuId, "image/png", f)

        # set the default rich menu
        line_bot_api.set_default_rich_menu(richMenuId)

        result = True

    except Exception:
        result = False

    return result
