from flask_restplus import Resource, Namespace
from ..services.auth_services import login
from app.main.auth.decorators import token_required

api = Namespace('Authentication', description='authentication framework')


@api.route('/login')
class UserLogin(Resource):
    @api.doc('login')
    @api.response(200, 'User successfully logged.')
    @api.response(201, 'User first log on platform, created db entry.')
    @api.response(401, 'Invalid credentials')
    @token_required
    def get(self, token, user_id):
        """Login user"""
        print("user {} requested login".format(user_id))
        return login(token, user_id)
