import uuid
import hmac
from os import urandom


def get_uuid():
    uuid_string = str(uuid.uuid1()).replace('-', '')
    return uuid_string


def get_hmac(key=None, s=None, method='SHA1'):
    key = str(uuid.uuid1()).replace('-', '') if key is None else key
    s = urandom(64) if s is None else s

    return hmac.new(key.encode('utf-8'), s, method).hexdigest()
