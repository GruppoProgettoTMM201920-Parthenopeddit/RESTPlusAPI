import requests

from config import BYPASS_LOGIN


def token_is_valid(token):
    if BYPASS_LOGIN:
        print("bypassed token_validation_request")
        return True

    s = requests.Session()
    s.headers.update({'authorization': 'Basic {}'.format(token)})
    r = s.get('https://api.uniparthenope.it/auth/v1/login')
    return r.status_code == 200


def login_request(token):
    if BYPASS_LOGIN:
        print("bypassed login_request")
        return {"dev": True}, 200

    s = requests.Session()
    s.headers.update({'authorization': 'Basic {}'.format(token)})
    r = s.get('https://api.uniparthenope.it/UniparthenopeApp/v1/login')
    return r.json(), r.status_code
