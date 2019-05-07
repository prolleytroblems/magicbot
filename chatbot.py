import base64
import hashlib
import hmac


def verify_source(body_bytestr, xline_signature, channel_secret):
    hash = hmac.new(channel_secret.encode('utf-8'), body_bytestr, hashlib.sha256).digest()
    signature = base64.b64encode(hash)

    return signature==xline_signature
