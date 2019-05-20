import json
import time

import requests

CUBE_URL = 'https://manaburn.org/wizards/delouge/cubes/b47acf4/list'
DRAFT_URL = 'https://manaburn.org/wizards/delouge/cubes/b47acf4/drafts'


def get_card(cardname):
    cardname = cardname.replace(" ", "%20").replace("'", "%27").replace('/', '%2F')
    response = requests.get("https://api.scryfall.com/cards/search?q="+cardname)
    if response.ok:
        time.sleep(0.1)
        content = json.loads(response.content)["data"][0]
        if content['layout']=='normal' or content['layout']=='meld' or content['layout']=='split':
            uris = content["image_uris"]
        elif content['layout']=='transform':
            found = False
            for face in content['card_faces']:
                if cardname.lower() in face['name'].lower():
                    uris = face["image_uris"]
                    found = True
            if not found:
                uris = content['card_faces'][0]['image_uris']
    else:
        print(response.content)
        return None

    image_url = uris["large"]
    preview_url = uris["small"]
    print(uris)
    return (image_url, preview_url)
