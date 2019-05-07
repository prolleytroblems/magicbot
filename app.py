import time
import json

from flask import Flask, jsonify, make_response, request
import requests

from chatbot import verify_source


app = Flask(__name__)

CHANNEL_SECRET = '99a7817c6e0604a686d21762b383d841'
ACCESS_TOKEN="mnWXUykYKquGDtTsP/4huxp4xkDIratVILDd/Ep4gSRxC4IIF9hOWFd3WMVi2J261MEVT0rTgoBWf0b4IbU1ttLhvsvHTi6KIj5PwNQRSoLa6XPapgZLmAME8lYXdCmxSw+JtLuWMroDeRSekMIxJwdB04t89/1O/w1cDnyilFU="



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

@app.route('/webhook', methods=['POST'])
def hook_home():
    print(request.get_json())

    #Make sure the body is not too big (100kB limit)
    assert request.content_length < 100000
    body = request.get_data()
    headers = request.headers

    print(verify_source(body, headers['X-Line-Signature'], CHANNEL_SECRET))
    """responses = {
        "message": message,
        "follow": follow,
        "join": join
    }"""
    return jsonify({'womp':'womp'})


if __name__=="__main__":
    app.run()
