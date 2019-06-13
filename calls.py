import json
import random

from commfuncs import *
from mtg import *
from linednd import *
from msgParser import set_macro, parse_text


NO_CHIN = [
    'https://i.kym-cdn.com/entries/icons/original/000/021/465/1476153817501.jpg',
    'https://upload.wikimedia.org/wikipedia/en/5/56/Mr_Burns.png',
    'https://vignette.wikia.nocookie.net/lifeofheroesrp/images/8/82/Ed.png/revision/latest?cb=20130413184918',
    'https://vignette.wikia.nocookie.net/fairlyoddfanon/images/3/30/DENZEL_COCKER.jpg/revision/latest/scale-to-width-down/173?cb=20120610053046'
]

def insultar_gnomo(*args, **kwargs):
    if random.random()>0.95:
        insultos=['cocozento', 'cheirador de cueca', 'gordo', 'gnomeu', 'Paris Hilton', 'boiola', 'fedorento', 'o pior jogador de magic',
                    'cheira-cola', 'sem-vergonha', 'descascador de batata', 'eletricista', 'bobao', 'pau no cu', 'babaca', 'vacilao',
                    'baka', 'kisama', 'pumpunzento', 'mago verde']
        return('You wrote: "gnomo". Did you mean: "'+random.choice(insultos)+'"?.')

def insultar_cadu(*args, **kwargs):
    if random.random()>0.95:
        return(random.choice(NO_CHIN))

def good_bot(*args, **kwargs):
    if random.random()>0.5:
        respostas = ['vsf seu arrombado, boa é sua mãe', 'brigado <3', 'valeu broder', 'prefiro uma nota de 20 que sua gratidão']
        return(random.choice(respostas))

def cardsearch(inputs, *args, **kwargs):
    msgs = []
    n=0
    try:
        image = get_card(inputs)
        if image is not None:
            msgs.append(image_msg(image))
            n+=1
        if n==5:
            return(msgs)
    except Exception as E:
        print(E)
    if len(msgs)>0:
        return(msgs)

def roll_long(inputs, *args, **kwargs):
    return str(roll(inputs[1:]))

def roll_dice(inputs, *args, **kwargs):
    return('\n'.join([str(roll(params)) for params in inputs]))

def roll_once(inputs, *args, **kwargs):
    return str(roll(inputs))

def echo(inputs, *args, **kwargs):
    return(inputs[1])

def macro(inputs, *args, **kwargs):
    out = set_macro(inputs)
    return(out)

def echo(inputs, *args, **kwargs):
    return(inputs[1])

def dndprocess(inputs, *args, **kwargs):
    return [process_msg(text.strip(), patterns='dnd') for text in inputs.split(';')]

def set_var():
    pass

def clear():
    pass

def clearall():
    pass

def follow():
    pass

def join():
    pass
