import base64
import hashlib
import hmac
import json
import time
import random

import requests
from flask import Response
from werkzeug.exceptions import Unauthorized

from msgParser import parse_text

CUBE_URL = 'https://manaburn.org/wizards/delouge/cubes/b47acf4/list'
DRAFT_URL = 'https://manaburn.org/wizards/delouge/cubes/b47acf4/drafts'

NO_CHIN = [
    'https://i.kym-cdn.com/entries/icons/original/000/021/465/1476153817501.jpg',
    'https://upload.wikimedia.org/wikipedia/en/5/56/Mr_Burns.png',
    'https://vignette.wikia.nocookie.net/lifeofheroesrp/images/8/82/Ed.png/revision/latest?cb=20130413184918',
    'https://vignette.wikia.nocookie.net/fairlyoddfanon/images/3/30/DENZEL_COCKER.jpg/revision/latest/scale-to-width-down/173?cb=20120610053046'
]

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
        'gnomo': (insultar_gnomo, (reply_token, access_token)),
        'goodbot': (good_bot, (reply_token, access_token)),
        'cadu': (insultar_cadu, (reply_token, access_token))
    }

    results = parse_text(message)
    print(results)

    for job in results:
        functions[job][0](*functions[job][1], inputs=results[job])
        print(job)

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

def follow():
    pass

def join():
    pass

def insultar_gnomo(reply_token, access_token, *args, **kwargs):
    if random.random()>0.6:
        insultos=['cocozento', 'cheirador de cueca', 'gordo', 'gnomeu', 'Paris Hilton', 'boiola', 'fedorento', 'o pior jogador de magic',
                    'cheira-cola', 'sem-vergonha', 'descascador de batata', 'eletricista', 'bobao', 'pau no cu', 'babaca', 'vacilao',
                    'baka', 'kisama', 'pumpunzento', 'mago verde']
        text_reply('You wrote: "gnomo". Did you mean: "'+random.choice(insultos)+'"?.', reply_token, access_token)
    else:
        return Response()

def insultar_cadu():
    if random.random()>0.7:
        text_reply(random.choice(NO_CHIN), reply_token, access_token)
    else:
        return Response()

def good_bot(reply_token, access_token, *args, **kwargs):
    if random.random()>0.5:
        respostas = ['vsf seu arrombado, boa é sua mãe', 'brigado <3', 'valeu broder', 'prefiro uma nota de 20 que sua gratidão']
        text_reply(random.choice(respostas), reply_token, access_token)
    else:
        return Response()

def cardsearch(reply_token, access_token, inputs, *args, **kwargs):
    print(inputs)
    msgs = []
    for input in inputs:
        image = get_card(input)
        msgs.append(image_msg(image))
    send_reply(msgs, reply_token, access_token, *args, **kwargs)

def get_card(cardname):
    response = requests.get("https://api.scryfall.com/cards/search?q="+cardname.replace(" ", "%20").replace("'", "%27"))
    if response.ok:
        time.sleep(0.1)
        content = json.loads(response.content)["data"][0]
        if content['layout']=='normal' or content['layout']=='meld' or content['layout']=='split':
            uris = content["image_uris"]
            image_url = uris["large"]
            preview_url = uris["small"]
            return (image_url, preview_url)
        elif content['layout']=='transform':
            for face in content['card_faces']:
                if cardname.lower() in face['name'].lower():
                    uris = face["image_uris"]
                    image_url = uris["large"]
                    preview_url = uris["small"]
                    return (image_url, preview_url)
    else:
        print(response.content)
        return None
