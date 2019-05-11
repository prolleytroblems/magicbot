import re

PATTERNS = {
    'cube': r'bot.*(cube|cubo)',
    'draft': r'bot.*(draft)',
    'card': r"\[([\w ]*?)\]"
    'gnomo': r'gnomo'
}

def parse_text(text):
    #patterndict is a dict of obj: patterns, outputs obj: result from re
    text = text.lower()
    out = {}
    for thing in PATTERNS:
        results = re.findall(text, PATTERNS[thing])
        if len(results) >0:
            out[thing]sdf[] = results
    return out
