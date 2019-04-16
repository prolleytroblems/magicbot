import time
import json

from flask import Flask, jsonify, make_response
import requests

app = Flask(__name__)



@app.route('/<string:cardname>')
def home(cardname):
    response = requests.get("https://api.scryfall.com/cards/search?q="+cardname.replace(" ", "%20"))
    if response.ok:
        time.sleep(0.1)
        image_url = json.loads(response.content)["data"][0]["image_uris"]["normal"]
        response = requests.get(image_url)
        response = make_response(response.content)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='card.png')
        return response
    else:
        return "Womp womp"

if __name__=="__main__":
    app.run()
