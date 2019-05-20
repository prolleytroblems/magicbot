import json
import random

from commfuncs import *
from mtg import *
from linednd import *

def insultar_gnomo(reply_token, access_token, *args, **kwargs):
    if random.random()>0.6:
        insultos=['cocozento', 'cheirador de cueca', 'gordo', 'gnomeu', 'Paris Hilton', 'boiola', 'fedorento', 'o pior jogador de magic',
                    'cheira-cola', 'sem-vergonha', 'descascador de batata', 'eletricista', 'bobao', 'pau no cu', 'babaca', 'vacilao',
                    'baka', 'kisama', 'pumpunzento', 'mago verde']
        text_reply('You wrote: "gnomo". Did you mean: "'+random.choice(insultos)+'"?.', reply_token, access_token)

def insultar_cadu(reply_token, access_token, *args, **kwargs):
    if random.random()>0.7:
        text_reply(random.choice(NO_CHIN), reply_token, access_token)

def good_bot(reply_token, access_token, *args, **kwargs):
    if random.random()>0.5:
        respostas = ['vsf seu arrombado, boa é sua mãe', 'brigado <3', 'valeu broder', 'prefiro uma nota de 20 que sua gratidão']
        text_reply(random.choice(respostas), reply_token, access_token)

def cardsearch(reply_token, access_token, inputs, *args, **kwargs):
    print(inputs)
    msgs = []
    for input in inputs:
        image = get_card(input)
        if image is None:
            msgs.append(image_msg(image))
    send_reply(msgs, reply_token, access_token, *args, **kwargs)

def follow():
    pass

def join():
    pass
