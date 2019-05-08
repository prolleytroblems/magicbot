import base64
import hashlib
import hmac
import json
import time

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
        #make this on a separate thread
        reply('You wrote: "gnomo". Did you mean: "cocozento?".', reply_token, access_token)

    """tasks = parse_message(event)
    for task in tasks:
        task['func'](event, access_token)
        """

def parse_message(event):
    message = event['message']['text']


def reply(text, reply_token, access_token):
    headers = {
        'Authorization': 'Bearer '+access_token,
        'Content-Type': 'application/json'
    }

    data = {
        'replyToken': reply_token,
        'messages': [
            {
                'type': 'text',
                'text': text
            }
        ]
    }
    try:
        response = requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, data=json.dumps(data))
    except Exception as E:
        print(E)

def follow():
    pass

def join():
    pass

def get_card(cardname):
    response = requests.get("https://api.scryfall.com/cards/search?q="+cardname.replace(" ", "%20"))
    if response.ok:
        time.sleep(0.1)
        uris = json.loads(response.content)["data"][0]["image_uris"]
        image_url = uris["large"]
        preview_url = uris
        response = requests.get(image_url)
        response = make_response(response.content)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='card.png')
        return response
    else:
        return Response()
