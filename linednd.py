import random

def roll(rollargs):
    out = 0
    for _ in range(rollargs[0]):
        out += int(random.random()*rollargs[1])+1
    if rollargs[3] == '+':
        out = out + rollargs[4]
    elif rollargs[3] == '-':
        out = out - rollargs[4]
    return out
