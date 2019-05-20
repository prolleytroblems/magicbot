import random

def roll(rollargs):
    print(rollargs)
    out = 0
    if rollargs[0]=='':
        rollargs[0]=1
    for _ in range(int(rollargs[0])):
        out += int(random.random()*int(rollargs[1]))+1
    if rollargs[3] == '+':
        out = out + int(rollargs[4])
    elif rollargs[3] == '-':
        out = out - int(rollargs[4])
    return out
