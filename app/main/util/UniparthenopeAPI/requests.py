import requests


def token_is_valid(token):
    s = requests.Session()
    s.headers.update({'authorization': 'Basic {}'.format(token)})
    r = s.get('https://api.uniparthenope.it/auth/v1/login')
    return r.status_code == 200


def login_request(token):
    s = requests.Session()
    s.headers.update({'authorization': 'Basic {}'.format(token)})
    r = s.get('https://api.uniparthenope.it/UniparthenopeApp/v1/login')
    return r.json(), r.status_code
