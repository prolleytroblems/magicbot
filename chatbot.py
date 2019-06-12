import base64
import hashlib
import hmac
import json

from flask import Response
from werkzeug.exceptions import Unauthorized

from msgParser import *
from calls import *
from mtg import *


def verify_source(body_bytestr, headers, channel_secret):
    hash = hmac.new(channel_secret.encode('utf-8'), body_bytestr, hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if signature!=headers['X-Line-Signature'].encode('utf-8'):
        raise Unauthorized(description="Not from Line!")

def message(event, headers, access_token):
    assert event['type']=='message'
    reply_token = event['replyToken']
    message = event['message']['text']

    process_msg(message, reply_token, access_token)


def process_msg(message, reply_token, access_token, **kwargs):
    functions = {
        'cube': (text_reply, (CUBE_URL, reply_token, access_token)),
        'draft': (text_reply, (DRAFT_URL, reply_token, access_token)),
        'card': (cardsearch, (reply_token, access_token)),
        'gnomo': (insultar_gnomo, (reply_token, access_token)),
        'goodbot': (good_bot, (reply_token, access_token)),
        'cadu': (insultar_cadu, (reply_token, access_token)),
        'roll': (roll_dice, (reply_token, access_token)),
        'macro': (macro, (reply_token, access_token))
    }

    results = parse_text(message, **kwargs)
    print(results)

    order = ['macro','roll','card','cube','draft','gnomo','cadu','goodbot']
    for job in order:
        if job in results:
            functions[job][0](*functions[job][1], inputs=results[job], **kwargs)
