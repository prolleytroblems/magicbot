import base64
import hashlib
import hmac
import json
import time
import random

import requests

from werkzeug.exceptions import Unauthorized

from msgParser import parse_text

CUBE_URL = 'https://manaburn.org/wizards/delouge/cubes/b47acf4/list'
DRAFT_URL = 'https://manaburn.org/wizards/delouge/cubes/b47acf4/drafts'

def verify_source(body_bytestr, headers, channel_secret):
    hash = hmac.new(channel_secret.encode('utf-8'), body_bytestr, hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if signature!=headers['X-Line-Signature'].encode('utf-8'):
        raise Unauthorized(description="Not from Line!")

def message(event, headers, access_token):
    assert event['type']=='message'

    reply_token = event['replyToken']
    message = event['message']['text']

    functions = {
        'cube': (text_reply, (CUBE_URL, reply_token, access_token)),
        'draft': (text_reply, (DRAFT_URL, reply_token, access_token)),
        'card': (cardsearch, (reply_token, access_token)),
        'gnomo': (insultar_gnomo, (reply_token, access_token))
    }

    results = parse_text(message)

    for job in results:
        functions[job][0](*functions[job[1]], inputs=results[job])

    for task in tasks:
        task['func'](event, access_token)


def text_reply(text, reply_token, access_token, *args, **kwargs):
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

def image_reply(image, reply_token, access_token, *args, **kwargs):
    headers = {
        'Authorization': 'Bearer '+access_token,
        'Content-Type': 'application/json'
    }

    data = {
        'replyToken': reply_token,
        'messages': [
            {
                'type': 'image',
                'originalContentUrl': image[0],
                'previewImageUrl': image[1]
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

def insultar_gnomo(text, reply_token, access_token, *args, **kwargs):
    insultos=['cocozento', 'cheirador de cueca', 'gordo', 'gnomeu', 'Paris Hilton', 'boiola', 'fedorento', 'o pior jogador de magic',
                'cheira-cola', 'sem-vergonha', 'descascador de batata', 'eletricista', 'bobao', 'pau no cu', 'babaca', 'vacilao']
    text_reply('You wrote: "gnomo". Did you mean: "'+random.choice(insultos)+'"?.', reply_token, access_token)

def cardsearch(reply_token, access_token, inputs, *args, **kwargs):
    for input in inputs:
        image = get_card(input)
        image_reply(image, reply_token, access_token, *args, **kwargs)

def get_card(cardname):
    response = requests.get("https://api.scryfall.com/cards/search?q="+cardname.replace(" ", "%20").replace("'", "%27"))
    if response.ok:
        time.sleep(0.1)
        uris = json.loads(response.content)["data"][0]["image_uris"]
        image_url = uris["large"]
        preview_url = uris["small"]
        return (image_url, preview_url)
    else:
        return None
