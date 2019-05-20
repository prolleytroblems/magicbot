import re
import json

PATTERNS = {
    'cube': r'bot.*(cube|cubo)',
    'draft': r'bot.*(draft)',
    'card': r"""\[([\w "\-'/]*?)\]""",
    'gnomo': r'gnomo',
    'goodbot': r'good.*bot',
    'cadu': r'(cadu|kadu)',
    'roll': r'([\d]{0,2})d([\d]{1,3})((\+|\-)(\d+))?',
    'macro': r'<(.*?):(.*?)>'
}

def parse_text(text):
    #patterndict is a dict of obj: patterns, outputs obj: result from re
    MACROS = json.load(open('macros.txt', 'r'))
    print('macros', MACROS)
    for macro in MACROS:
        text = re.sub(macro, MACROS[macro], text)

    text = text.lower()
    out = {}
    for thing in PATTERNS:
        results = re.findall(PATTERNS[thing], text)
        if len(results) >0:
            out[thing]= results
    return out

def set_macro(inputs):
    full = json.load(open('macros.txt', 'r'))
    out = ''
    for input in inputs:
        full[input[0].lower()] = input[1].lower()
        out += "Set macro: '{}' -> '{}' \n".format(input[0], input[1])
    json.dump(full, open('macros.txt', 'w'))
    return out
