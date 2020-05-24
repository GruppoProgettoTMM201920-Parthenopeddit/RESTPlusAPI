from functools import wraps

from flask import request

from app.main.util.UniparthenopeAPI.requests import token_is_valid
from app.main.util.token_encoding import token_decode_username
from app.main.model.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'authorization' not in request.headers:
            return {
                'status': 'error',
                'message': 'Authorization token missing'
            }, 451

        auth = request.headers['authorization']
        token = auth.split()[1]

        user_id = token_decode_username(token)

        return f(*args, **kwargs, token=token, user_id=user_id)
    return decorated


def login_required(api):
    def wrapper_func(f):
        @api.response(451, 'Authorization token missing')
        @api.response(452, 'Invalid credentials')
        @api.response(453, 'Login required')
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'authorization' not in request.headers:
                return {
                           'status': 'error',
                           'message': 'Authorization token missing'
                       }, 451
            auth = request.headers['authorization']
            token = auth.split()[1]
            if not token_is_valid(token):
                return {
                           'status': 'error',
                           'message': 'Invalid token'
                       }, 452
            user_id = token_decode_username(token)
            user = User.query.filter(User.id == user_id).first()
            if not user:
                return {
                           'status': 'error',
                           'message': 'Login required'
                       }, 453
            return f(*args, **kwargs, user=user)

        return decorated

    return wrapper_func





