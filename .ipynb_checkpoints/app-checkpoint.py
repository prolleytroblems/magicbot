import time
import json

from flask import Flask, jsonify, make_response, request, Response
import requests

from chatbot import verify_source, message, follow, join

from keys import *

app = Flask(__name__)


@app.route('/<string:cardname>')
def home(cardname):
    return "Womp womp"

@app.route('/webhook', methods=['POST'])
def hook_home():
    #Make sure the body is not too big (100kB limit)
    assert request.content_length < 100000
    body = request.get_data()
    headers = request.headers

    verify_source(body, headers, CHANNEL_SECRET)

    body = json.loads(body.decode('utf-8'))
    response_funcs = {
        "message": message,
        "follow": follow,
        "join": join
    }

    for event in body['events']:
        if event['type'] not in response_funcs:
            pass
        else:
            response_funcs[event['type']](event, headers, ACCESS_TOKEN)

    return Response()


if __name__=="__main__":
    app.run()
