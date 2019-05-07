import base64
import hashlib
import hmac


def verify_source(body_bytestr, headers, channel_secret):
    hash = hmac.new(channel_secret.encode('utf-8'), body_bytestr, hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    return signature==headers['X-Line-Signature'].encode('utf-8')

def message(body_bytestr, headers):
    assert headers['type']=='message'

    reply_token = headers['replyToken']
