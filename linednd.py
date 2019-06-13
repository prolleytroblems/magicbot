import random

def roll(rollargs):
    print(rollargs)
    args = []

    for i in rollargs:
        try:
            args.append(int(i))
        except ValueError as E:
            args.append(i)
    if args[0]=='':
        args[0]=1

    out = 0
    for _ in range(args[0]):
        out += int(random.random()*args[1])+1

    special = None
    if args[1]==20:
        if out == 20:
            special = 'Critical success! '
        elif out == 1:
            special = 'Critical FAILURE! '

    if rollargs[3] == '+':
        out = out + args[4]
    elif rollargs[3] == '-':
        out = out - args[4]

    if special is None:
        return out
    else:
        return special + str(out)
