import re
import json

PATTERNS = {
    'cube': r'bot.*(cube|cubo)',
    'draft': r'bot.*(draft)',
    'card': r"""\[([\w "\-'/]*?)\]""",
    'gnomo': r'gnomo',
    'goodbot': r'good.*bot',
    'cadu': r'(cadu|kadu)',
    'dnd': r'<(.*?)>',
    'set_macro':'!s(et)? (.+):"(.+?)"'
}

DND_PATTERNS = {
    'set_var':'!v(ar)? (.+)',
    'echo':'!e(cho)? (.+)',
    'clear':'!c(lear)? (.+)',
    'clear_all':'!clearall',
    'roll': r'([\d]{0,2})d([\d]{1,3})((\+|\-)(\d+))?',

}
#add: reset macros, show all macros, titles on macros, make different functions add to the same reply

def parse_text(text, patterns = 'normal'):
    #patterndict is a dict of obj: patterns, outputs obj: result from re
    print("Parse call, text: '{}', mode: {}".format(text, patterns))
    out = []
    text = text.lower()

    MACROS = json.load(open('macros.txt', 'r'))
    for macro in MACROS:
        if macro in text:
            start, end = re.search(macro, text).span()
            newtext = text[:start]+MACROS[macro]+text[end:]
            return parse_text(newtext)

    if patterns == 'normal':
        patpats = PATTERNS
    elif patterns == 'dnd':
        patpats = DND_PATTERNS
    else:
        raise ValueError()

    for thing in patpats:
        results = re.findall(patpats[thing], text)
        for r in results:
            out.append((thing, r))

    print(out)
    return out


def set_macro(inputs, *args, **kwargs):
    full = json.load(open('macros.txt', 'r'))
    out = ''
    if '#' not in inputs[2]:
        full['#'+inputs[1].strip().lower()] = inputs[2]
        out += "Set macro: '{}' -> '{}' \n".format(inputs[1], inputs[2])
    else:
        out += "No recursion: remove the # from your macro you sneaky shit. \n"
    json.dump(full, open('macros.txt', 'w'))
    return out

def clear_macro(inputs, *args, **kwargs):
    return set_macro([(inputs[1])])

def clear_all(*args, **kwargs):
    json.dump({}, open('macros.txt', 'w'))
    return "Macros cleared."
