import base64
import hashlib
import hmac
import json

from flask import Response
from werkzeug.exceptions import Unauthorized

from msgParser import parse_text
from linednd import roll
from calls import *
from mtg import *
from commfuncs import *


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
