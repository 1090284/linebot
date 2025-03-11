from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TemplateMessage,
    PushMessageRequest,
    BroadcastRequest,
    MulticastRequest,
    TextMessage,
    Emoji,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    FlexMessage,
    FlexBubble,
    FlexImage,
    FlexMessage,
    FlexBox,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer,
    URIAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import json

import openai
from openai import OpenAI
from dotenv import dotenv_values

app = Flask(__name__)

configuration = Configuration(access_token='Bwj7yl23jpDQpwH9NPZb758hP/l4gdPzkwwcFa4pjvuz4dKWthMXfhS/pBTALFKn5aoeFap9iSYcaQ9ZDq450lB439CEJhG7apuf/8jwQ0GYw+tS9mq3UD8Ptu633jY5ORx64dg2HjkJoHzH6nDimgdB04t89/1O/w1cDnyilFU=')
line_handler = WebhookHandler('35c892a83dd6c9296ee284351831f5cc')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#加入好友事件
# @handler.add(FollowEvent)
# def hander_follow(event):
#     print(f'Got {event.type} event')
config = dotenv_values('.env')
client = OpenAI(api_key=config["API_KEY"])
#訊息事件
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # reply message
        # line_bot_api.reply_message(
        #     ReplyMessageRequest(
        #     reply_token=event.reply_token,
        #     # messages=[TextMessage(text='Hello world')]
        #     res = client.completions.create(
        #         model="gpt-3.5-turbo-instruct",
        #         prompt=text,
        #         max_tokens=500,
        #         temperature=0
        #         )
        #      messages=[TextMessage(text=res.choices[0].text)]
        #     )
        # )

        #test
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    response_text = get_openai_response(text)
    reply_to_user(event.reply_token, response_text)

def get_openai_response(prompt):
    try:
        res = client.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=500,
            temperature=0
        )
        return res.choices[0].text.strip()
    except Exception as e:
        app.logger.error(f"OpenAI API call failed: {e}")
        return "对不起，我无法处理您的请求。"

def reply_to_user(reply_token, text):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        try:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=text)]
                )
            )
        except Exception as e:
            app.logger.error(f"Failed to send reply: {e}")

        #test
        
        
        # if event.message.text == 'postback':
        #     buttons_template = ButtonsTemplate(
        #         title='Postback Sample',
        #         text='Postback Action',
        #         actions=[
        #             PostbackAction(label='postback',TEXT='Postback Action Button Clicked!', data='postback'),
        #         ])
        #     template_message = TemplateMessage(
        #         alt_text='Postback Sample', 
        #         template=buttons_template
        #     )
        #     line_bot_api.reply_message(
        #         reply_token=event.reply_token,
        #         messages=[template_message]
        #     )
            
        # result = line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text = "reply message with http info")]#linebot回應的訊息設定:可以點result看回傳的code
        #     )
        # )


        # push message
        # line_bot_api.push_message_with_http_info(
        #     PushMessageRequest(
        #         to=event.source.user_id,
        #         messages=[TextMessage(text='push')]
        #     )
        # )

        # broadcast message
        # line_bot_api.broadcast_with_http_info(
        #     BroadcastRequest(
        #         messages=[TextMessage(text='broadcast')]
        #     )
        # )

        # multicast message
        # line_bot_api.multicast_with_http_info(
        #     MulticastRequest(
        #         to=['U4eb1f312bef48af3c27f2892dd72c4c1'],
        #         messages=[TextMessage(text='multicast')],
        #         notificationDisabled=True #靜音通知
        #     )
        # )

        # #文字訊息
        if text == "文字":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="Hello, world!")]
                )
            )
        # #表情符號
        # elif text == "表情符號":
        #     emojis = [
        #             Emoji(index=0, productId='5ac1bfd5040ab15980c9b435', emojiId='001'),
        #             #index:表情符號的位置
        #             #productId:表情符號的ID 在LINE開發者網站product emojis上可以找到
        #             Emoji(index=12, productId='5ac1bfd5040ab15980c9b435', emojiId='002'),
        #              ]
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[TextMessage(text="$ LINE 表情符號 $",emojis=emojis)]
        #             # $ LINE 表情符號 $ 會顯示表情符號
        #             )
        #     )
        # #貼圖訊息
        # elif text == "貼圖":
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[StickerMessage(package_id='446', sticker_id='1988')]#同表情符號用法
        #         )
        #     )
        # # #圖片訊息
        # elif text == "圖片":
        #     url = request.url_root + 'static/Clipped_image_20240121_2228262.png'
        #     url = url.replace('http', 'https')
        #     app.logger.info("url=" + url)
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[ImageMessage(original_content_url=url, preview_image_url=url)]
        #         )
        #     )
        # # #影片訊息
        # elif text == "影片":
        #     url = request.url_root + 'static/2024-08-08 20-28-00.mp4'
        #     url = url.replace('http', 'https')#LINE只接受https
        #     app.logger.info("url=" + url)
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[VideoMessage(original_content_url=url, preview_image_url=url)]
        #         )
        #     )
        # #音訊訊息
        # elif text == "音訊":
        #     url = request.url_root + 'static/audio_en.mp3'
        #     url = url.replace('http', 'https')
        #     app.logger.info("url=" + url)
        #     duration = 10000 #音訊長度(毫秒)
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[AudioMessage(original_content_url=url, duration=duration)]
        #         )
        #     )
        # #位置訊息
        # elif text == "位置":
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[LocationMessage(title='location', address='Tokyo', latitude=35.65910807942215, longitude=139.70372892916203)]
        #             #title:標題
        #             #address:地址
        #             #latitude:緯度
        #             #longitude:經度
        #         )
        #     )
        # # ComfirmTemplate 
        # if text == "confirm":
        #     confirm_template = ConfirmTemplate(
        #         text='你今天學程式了嗎?',#問題
        #         actions=[
        #             MessageAction(label='Yes', text='Yes!'),#(label:按鈕名稱,text:回傳的文字)
        #             MessageAction(label='No', text='No!')#(label:按鈕名稱,text:回傳的文字)
        #         ]
        #     )
        #     template_message = TemplateMessage(
        #         alt_text='Confirm alt text',#傳送給使用者會接受到的文字 
        #         template=confirm_template#哪一種模板訊息
        #     )
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[template_message]
        #         )
        #     )
        # # ButtonsTemplate
        # elif text == "buttons":
        #     url = request.url_root + 'static/Clipped_image_20240121_2228262.png'
        #     url = url.replace('http', 'https')
        #     app.logger.info("url=" + url)
        #     buttons_template = ButtonsTemplate(
        #         thumbnail_image_url=url,
        #         title='示範',
        #         text='詳細說明',
        #         actions=[
        #             MessageAction(label='傳"哈囉"', text='哈囉'),
        #             URIAction(label='連結', uri='https://www.youtube.com/watch?v=ObpJUn1Kd7E&list=RDObpJUn1Kd7E&start_radio=1'),
        #             PostbackAction(label='回傳值', data='ping', displayText="傳了"),#displayText不會傳送訊息事件回伺服器),
        #             DatetimePickerAction(label='選擇時間', data='時間', mode='datetime'),
        #         ]
        #     )
        #     template_message = TemplateMessage(
        #         alt_text='This is a buttons template', 
        #         template=buttons_template
        #     )
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[template_message]
        #         )
        #     )
        # elif text == "carousel":
        #     url = request.url_root + 'static/Clipped_image_20240121_2228262.png'
        #     url = url.replace('http', 'https')
        #     app.logger.info("url=" + url)
        #     carousel_template = CarouselTemplate(
        #         columns=[
        #             CarouselColumn(
        #                 thumbnail_image_url=url,
        #                 title='第一項',
        #                 text='詳細說明1',
        #                 actions=[
        #                     URIAction(
        #                         label='連結1',
        #                         uri='https://www.youtube.com/watch?v=ObpJUn1Kd7E&list=RDObpJUn1Kd7E&start_radio=1'
        #                     ),
        #                 ]
        #             ),
        #             CarouselColumn(
        #                 thumbnail_image_url=url,
        #                 title='示範2',
        #                 text='詳細說明2',
        #                 actions=[
        #                     URIAction(
        #                         label='連結2',
        #                         uri='https://www.youtube.com/watch?v=RmE4ceciIOI&list=RDObpJUn1Kd7E&index=3'
        #                     ),
        #                 ])
        #         ]
        #     )
        #     carousel_message = TemplateMessage(
        #         alt_text='This is a carousel template', 
        #         template=carousel_template
        #     )
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[carousel_message]
        #         )
        #     )
        # elif text == "image carousel":
        #     url = request.url_root + 'static/Clipped_image_20240121_2228262.png'
        #     url = url.replace('http', 'https')
        #     app.logger.info("url=" + url)
        #     image_carousel_template = ImageCarouselTemplate(
        #         columns=[
        #             ImageCarouselColumn(
        #                 image_url=url,
        #                 action=URIAction(
        #                     label='連結1',
        #                     uri='https://www.youtube.com/watch?v=ObpJUn1Kd7E&list=RDObpJUn1Kd7E&start_radio=1'
        #                 )
        #             ),
        #             ImageCarouselColumn(
        #                 image_url=url,
        #                 action=URIAction(
        #                     label='連結2',
        #                     uri='https://www.youtube.com/watch?v=RmE4ceciIOI&list=RDObpJUn1Kd7E&index=3'
        #                 )
        #             )
        #         ]
        #     )
        #     image_carousel_message = TemplateMessage(
        #         alt_text='圖片輪播範本', 
        #         template=image_carousel_template
        #     )
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[image_carousel_message]
        #         )
        #     )
#     if text == 'flex.1':#使用LINE的模擬器flex simulator
#         line_flex_json = {
            
#   "type": "bubble",
#   "hero": {
#     "type": "image",
#     "size": "full",
#     "aspectRatio": "20:13",
#     "aspectMode": "cover",
#     "action": {
#       "type": "uri",
#       "uri": "https://line.me/"
#     },
#     "url": "https://drive.google.com/file/d/1-mj3D5c0GaxM7VpKUXX7_hYbQwDzOwB6/view?usp=sharing"
#   },
#   "body": {
#     "type": "box",
#     "layout": "vertical",
#     "contents": [
#       {
#         "type": "text",
#         "text": "Hi",
#         "weight": "bold",
#         "size": "xl"
#       },
#       {
#         "type": "box",
#         "layout": "baseline",
#         "margin": "md",
#         "contents": [
#           {
#             "type": "icon",
#             "size": "sm",
#             "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
#           },
#           {
#             "type": "icon",
#             "size": "sm",
#             "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
#           },
#           {
#             "type": "icon",
#             "size": "sm",
#             "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
#           },
#           {
#             "type": "icon",
#             "size": "sm",
#             "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
#           },
#           {
#             "type": "icon",
#             "size": "sm",
#             "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
#           },
#           {
#             "type": "text",
#             "text": "4.0",
#             "size": "sm",
#             "color": "#999999",
#             "margin": "md",
#             "flex": 0
#           }
#         ]
#       },
#       {
#         "type": "box",
#         "layout": "vertical",
#         "margin": "lg",
#         "spacing": "sm",
#         "contents": [
#           {
#             "type": "box",
#             "layout": "baseline",
#             "spacing": "sm",
#             "contents": [
#               {
#                 "type": "text",
#                 "text": "Place",
#                 "color": "#aaaaaa",
#                 "size": "sm",
#                 "flex": 1
#               },
#               {
#                 "type": "text",
#                 "text": "Flex Tower, 7-7-4 Midori-ku, Tokyo",
#                 "wrap": True,
#                 "color": "#666666",
#                 "size": "sm",
#                 "flex": 5
#               }
#             ]
#           },
#           {
#             "type": "box",
#             "layout": "baseline",
#             "spacing": "sm",
#             "contents": [
#               {
#                 "type": "text",
#                 "text": "Time",
#                 "color": "#aaaaaa",
#                 "size": "sm",
#                 "flex": 1
#               },
#               {
#                 "type": "text",
#                 "text": "10:00 - 23:00",
#                 "wrap": True,
#                 "color": "#666666",
#                 "size": "sm",
#                 "flex": 5
#               }
#             ]
#           }
#         ]
#       }
#     ]
#   },
#   "footer": {
#     "type": "box",
#     "layout": "vertical",
#     "spacing": "sm",
#     "contents": [
#       {
#         "type": "button",
#         "style": "link",
#         "height": "sm",
#         "action": {
#           "type": "uri",
#           "label": "CALL",
#           "uri": "https://line.me/"
#         }
#       },
#       {
#         "type": "button",
#         "style": "link",
#         "height": "sm",
#         "action": {
#           "type": "uri",
#           "label": "WEBSITE",
#           "uri": "https://line.me/"
#         }
#       },
#       {
#         "type": "box",
#         "layout": "vertical",
#         "contents": [],
#         "margin": "sm"
#       }
#     ],
#     "flex": 0
#   }
# }
        
#         line_flex_str = json.dumps(line_flex_json)
#         line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[FlexMessage(alt_text='詳細說明', contents=FlexContainer.from_json(line_flex_str))]
#             )
#         )
#     else:
#         line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=event.message.text)]
#             )
#         )
#沒有imagemap
#沒有Quick reply
#沒有Rich menu


# @handler.add(PostbackEvent)
# def handle_postback(event):
#     if event.postback.data == 'postback':
#         print('Postback event is triggered')
if __name__ == "__main__":
    app.run()
