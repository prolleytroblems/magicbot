import random

def roll(rollargs):
    out = 0
    if rollargs[0]==''
        rollargs[0]=1
    for _ in range(int(rollargs[0])):
        out += int(random.random()*int(rollargs[1]))+1
    if int(rollargs[3]) == '+':
        out = out + int(rollargs[4])
    elif int(rollargs[3]) == '-':
        out = out - int(rollargs[4])
    return out
