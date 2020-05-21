from flask_restplus import Resource, Namespace

from app.main.namespaces.auth.auth_services import login
from app.main.util.auth_decorator import token_required
from app.main.namespaces.models_definition import get_complete_user_model

api = Namespace('Authentication', description='authentication framework')


@api.route('/login')
class UserLogin(Resource):
    @api.doc('login')
    @api.response(200, 'User successfully logged.')
    @api.response(201, 'User first log on platform, created db entry.')
    @api.response(451, 'Authorization token missing')
    @api.marshal_with(get_complete_user_model(api))
    @token_required
    def get(self, token, user_id):
        """Login user"""
        return login(token, user_id)
