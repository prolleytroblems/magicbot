import json
import random

from commfuncs import *
from mtg import *
from linednd import *
from msgParser import set_macro


NO_CHIN = [
    'https://i.kym-cdn.com/entries/icons/original/000/021/465/1476153817501.jpg',
    'https://upload.wikimedia.org/wikipedia/en/5/56/Mr_Burns.png',
    'https://vignette.wikia.nocookie.net/lifeofheroesrp/images/8/82/Ed.png/revision/latest?cb=20130413184918',
    'https://vignette.wikia.nocookie.net/fairlyoddfanon/images/3/30/DENZEL_COCKER.jpg/revision/latest/scale-to-width-down/173?cb=20120610053046'
]

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
        try:
            image = get_card(input)
            if image is not None:
                msgs.append(image_msg(image))
        except Exception as E:
            print(E)
    if len(msgs)>0:
        print(msgs)
        send_reply(msgs, reply_token, access_token, *args, **kwargs)

def roll_dice(reply_token, access_token, inputs, *args, **kwargs):
    msgs = []
    for params in inputs:
        msgs.append(text_msg(roll(params)))
    send_reply(msgs, reply_token, access_token, *args, **kwargs)

def macro(reply_token, access_token, inputs):
    out = ''
    for input in inputs:
        out += set_macro(input)
    send_reply([text_msg(out)], reply_token, access_token, *args, **kwargs)

def follow():
    pass

def join():
    pass
