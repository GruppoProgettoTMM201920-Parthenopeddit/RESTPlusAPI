from flask import request
from flask_restplus import Namespace, Resource

from app.main.namespaces.auth.auth_decorator import login_required
from app.main.namespaces.messages.messages_service import get_user_chats_with_users, get_user_chat_with_user, \
    send_message_to_user
from app.main.namespaces.models_definition import get_new_message_model, get_message_model, get_user_chat_model, \
    get_user_chat_model_with_log

api = Namespace('Messages', description='')


@api.route("/open_chats/users")
class ChatsWithUsers(Resource):
    @login_required(api)
    @api.marshal_list_with(get_user_chat_model(api, get_other_chat=True))
    def get(self, user):
        return get_user_chats_with_users(user)


@api.route("/chat/<string:user_id>")
class ChatWithUser(Resource):
    @login_required(api)
    @api.marshal_with(get_user_chat_model_with_log(api))
    def get(self, user, user_id):
        return get_user_chat_with_user(user, user_id)

    @login_required(api)
    @api.expect(get_new_message_model(api))
    @api.marshal_with(get_message_model(api))
    def post(self, user, user_id):
        return send_message_to_user(user, user_id, request)
