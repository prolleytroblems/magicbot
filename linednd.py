import random

def roll(rollargs):
    rollargs = list(rollargs)
    if rollargs[0]=='':
        rollargs[0]=1

    out = 0
    for _ in range(int(rollargs[0])):
        out += int(random.random()*int(rollargs[1]))+1
    if rollargs[3] == '+':
        out = out + int(rollargs[4])
    elif rollargs[3] == '-':
        out = out - int(rollargs[4])
    return out
