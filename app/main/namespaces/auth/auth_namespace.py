from flask import request
from flask_restplus import Resource, Namespace

from app.main.namespaces.auth.auth_services import login, register_new_token
from app.main.namespaces.models_definition import get_complete_user_model, get_new_device_token_model
from main.namespaces.auth.auth_decorator import token_required, login_required

api = Namespace('Authentication', description='authentication framework')


@api.route('/login')
class UserLogin(Resource):
    @api.doc('login')
    @api.response(200, 'User successfully logged.')
    @api.response(201, 'User first log on platform, created db entry.')
    @api.response(451, 'Authorization token missing')
    @api.response(452, 'Invalid credentials')
    @api.marshal_with(get_complete_user_model(api))
    @token_required
    def get(self, token, user_id):
        """Login user"""
        return login(token, user_id)


@api.route("/register_device_token")
class RegisterDeviceToken(Resource):
    @login_required(api)
    @api.expect(get_new_device_token_model(api))
    def post(self, user):
        print('registering')
        return register_new_token(user, request)
