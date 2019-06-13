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
    'dnd': r'<(.*?)>',
    'macro': '#(.*?) '
}

DND_PATTERNS = {
    'macro':'!set ',
    'var':'!var ',
    'echo':'',
    'clear':'',
    'clearall':'',

}
#add: reset macros, show all macros, titles on macros, make different functions add to the same reply

def parse_text(text, patterns = PATTERNS):
    #patterndict is a dict of obj: patterns, outputs obj: result from re
    out = []
    text = text.lower()

    MACROS = json.load(open('macros.txt', 'r'))
    extra_text=''
    for macro in MACROS:
        if macro in text:
            start, end = re.search(macro, text).span()
            newtext = text[:start]+MACROS[macro]+text[end:]
            return parse_text(newtext)

    for thing in PATTERNS:
        results = re.findall(PATTERNS[thing], text)
        results += re.findall(PATTERNS[thing], extra_text)
        for r in results:
            out.append((thing, r))

    return out

def set_macro(inputs):
    full = json.load(open('macros.txt', 'r'))
    out = ''
    for input in inputs:
        if '#' not in input[1]:
            full['#'+input[0].strip().lower()] = input[1]
            out += "Set macro: '{}' -> '{}' \n".format(input[0], input[1])
        else:
            out += "No recursion: remove the # from your macro you sneaky shit. \n"
    json.dump(full, open('macros.txt', 'w'))
    return out
