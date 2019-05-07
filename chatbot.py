import base64
import hashlib
import hmac
import json

import requests

from werkzeug.exceptions import Unauthorized

def verify_source(body_bytestr, headers, channel_secret):
    hash = hmac.new(channel_secret.encode('utf-8'), body_bytestr, hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if signature!=headers['X-Line-Signature'].encode('utf-8'):
        raise Unauthorized(description="Not from Line!")

def message(body, headers, access_token):
    assert body['type']=='message'

    reply_token = body['replyToken']
    if 'gnomo' in body['message']['text']:
        reply('Vai se fuder gnomo.', reply_token, access_token)
    #parse_message(body['message']['text'])


def reply(text, reply_token, access_token):
    headers = {
        'Authorization': 'Bearer '+access_token,
        'Content-Type': 'application/json'
    }

    data = {
        'replyToken': reply_token,
        'messages': {
            'type': 'text',
            'text': text
        }
    }
    requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, data=data)

def follow():
    pass

def join():
    pass
