import requests
import json

def text_reply(text, *args, **kwargs):
    send_reply([text_msg(text)], *args, **kwargs)

def send_reply(messages, reply_token, access_token, *args, **kwargs):
    assert isinstance(messages, list)
    headers = {
        'Authorization': 'Bearer '+access_token,
        'Content-Type': 'application/json'
    }

    data = {
        'replyToken': reply_token,
        'messages': messages
    }
    try:
        response = requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, data=json.dumps(data))
    except Exception as E:
        print(E)
        raise(E)

def text_msg(text):
    return {
        'type': 'text',
        'text': text
    }

def image_msg(image):
    return {
        'type': 'image',
        'originalContentUrl': image[0],
        'previewImageUrl': image[1]
    }
