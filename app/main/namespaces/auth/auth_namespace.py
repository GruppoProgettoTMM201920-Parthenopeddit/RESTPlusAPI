from flask import request
from flask_restplus import Resource, Namespace

from app.main.namespaces.auth.auth_services import login, register_new_token
from app.main.namespaces.models_definition import get_complete_user_model, get_new_device_token_model, \
    get_simple_user_model
from main.namespaces.auth.auth_decorator import token_required, login_required

api = Namespace('Authentication', description='authentication framework')


@api.route('/login')
class UserLogin(Resource):
    @api.response(456, 'Invalid credentials')
    @api.response(471, 'Not a student')
    @api.response(520, 'Deferred error - check result')
    @api.marshal_with(get_complete_user_model(api), code=200, description='User successfully logged.')
    @api.marshal_with(get_simple_user_model(api), code=201, description='User first log on platform, created db entry..')
    @token_required(api)
    def get(self, token, user_id):
        """Login user"""
        return login(token, user_id)


@api.route("/register_device_token")
class RegisterDeviceToken(Resource):
    @login_required(api)
    @api.response(452, 'Missing expected data')
    @api.response(200, 'Token already registered for user')
    @api.response(201, 'Token registered for user')
    @api.response(202, 'Changed token Owner')
    @api.expect(get_new_device_token_model(api))
    def post(self, user):
        """Register device token used in notifications"""
        return register_new_token(user, request)
