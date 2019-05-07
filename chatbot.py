import base64
import hashlib
import hmac


def verify_source(request_obj, channel_secret):
    #Make sure the body is not too big (100kB limit)
    assert request_obj.content_length < 100000
    body = request.get_data()
    hash = hmac.new(channel_secret.encode('utf-8'), body, hashlib.sha256).digest()
    signature = base64.b64encode(hash)

    return hash==signature
