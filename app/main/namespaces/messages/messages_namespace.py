from flask_restplus import Namespace, Resource

from app.main.util.auth_decorator import login_required

# TODO add description
api = Namespace('Messages', description='')


@api.route("/open_chats/users")
class ChatsWithUsers(Resource):
    @login_required(api)
    def get(self, user):
        return {}, 200