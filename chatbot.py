import base64
import hashlib
import hmac
import json

from flask import Response
from werkzeug.exceptions import Unauthorized

from msgParser import *
from calls import *
from mtg import *
from commfuncs import text_msg, send_reply


def verify_source(body_bytestr, headers, channel_secret):
    hash = hmac.new(channel_secret.encode('utf-8'), body_bytestr, hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if signature!=headers['X-Line-Signature'].encode('utf-8'):
        raise Unauthorized(description="Not from Line!")

def message(event, headers, access_token):
    assert event['type']=='message'
    reply_token = event['replyToken']
    message = event['message']['text']

    return_msg(reply_token, access_token, message)

def return_msg(reply_token, access_token, message, **kwargs):
    out, messages = process_msg(reply_token, access_token, message, **kwargs)
    messages.append(text_msg(out))
    print(messages)
    send_reply(reply_token, access_token, messages)

def process_msg(reply_token, access_token, inputs, **kwargs):
    functions = {
        'cube': (text_reply, (CUBE_URL)),
        'draft': (text_reply, (DRAFT_URL)),
        'card': (cardsearch, ()),
        'gnomo': (insultar_gnomo, ()),
        'goodbot': (good_bot, ()),
        'cadu': (insultar_cadu, ()),
        'roll': (roll_once, ()),
        'macro': (macro, ()),
        'echo': (echo, ()),
        'set_macro': (macro, ()),
        'set_var': (set_var, ()),
        'clear': (clear, ()),
        'clear_all': (clearall, ()),
        'roll_long': (roll_long, ()),
        'dnd': (process_msg, (reply_token, access_token))
    }

    results = parse_text(inputs, **kwargs)
    print(results)

    out = []
    messages = []
    for job, inputs in results:
        r = functions[job][0](*functions[job][1], inputs=inputs, **kwargs)
        if isinstance(r, str):
            out.append(r)
        elif isinstance(r, list):
            messages += r
        elif isinstance(r, dict):
            messages.append(r)
        elif r is None:
            pass
        else:
            raise TypeError('Something wrong with the call func output')

    out = '\n'.join(out)
    print(out, messages)
    return (out, messages)
