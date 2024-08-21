import json
import time
import base64
import hashlib


def get_secret_key():
    return 'AsjAUSJAUAnsakko3ajsnrfr_'


def generate(login):
    head = {
        "typ": "JWT",
        "alg": "HS256"
    }
    payload = {
        "exp": time.time() + 24 * 60 * 60,
        "sub": login,
        "sta": time.time()
    }
    data = base64.b64encode(str.encode(json.dumps(head))).decode() + "." + base64.b64encode(
        str.encode(json.dumps(payload))).decode()
    cert = hashlib.md5((get_secret_key() + json.dumps(payload)).encode()).hexdigest()
    return data + "." + cert


def check_correct_token(token):
    nodes = token.split('.')
    names = ['exp', 'sta', 'sub']
    if len(nodes) != 3:
        return False
    payload = json.loads(base64.b64decode(nodes[1]))

    for i in payload.keys():
        if i in names:
            names.remove(i)
    if len(names) != 0:
        return False
  #  if payload['exp'] < time.time():
   #     return False

    cert_from_token = hashlib.md5((get_secret_key() + json.dumps(payload)).encode()).hexdigest()

    if cert_from_token == nodes[2]:
        return True
    return False


def get_token_info(token):
    nodes = token.split('.')
    payload = json.loads(base64.b64decode(nodes[1]))
    payload['login'] = payload['sub']
    return payload
