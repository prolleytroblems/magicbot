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

def message(event, headers, access_token):
    assert event['type']=='message'

    reply_token = event['replyToken']
    if 'gnomo' in event['message']['text']:
        print('replying')
        #make this on a separate thread
        reply('Vai se fuder gnomo.', reply_token, access_token)

    """queue = parse_message(event['message']['text'])
    for task in queue:
        if task
        """

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
