import re

PATTERNS = {
    'cube': r'bot.*(cube|cubo)',
    'draft': r'bot.*(draft)',
    'card': r"""\[([\w "\-'/]*?)\]""",
    'gnomo': r'gnomo',
    'goodbot': r'good.*bot',
    'cadu': r'(cadu|kadu)',
    'roll': r'([\d]{0,2})d([\d]{1,3})((\+|\-)(\d+))?',
    'macro': r'<\w*?:\w*?>'
}


MACROS = {}


def parse_text(text, macros_patterns = None):
    #patterndict is a dict of obj: patterns, outputs obj: result from re
    for macro in macros_patterns:
        text = re.sub(macro, macros_patterns[macro], text)

    text = text.lower()
    out = {}
    for thing in PATTERNS:
        results = re.findall(PATTERNS[thing], text)
        if len(results) >0:
            out[thing]= results
    return out


def set_macro(input):
    macros[input[0]] = input[1]    
