from datetime import datetime

from app.main.model.user import User
from app.main.model.users_chat import UsersChat
from app.main import db
from app.main.util.extract_resource import extract_resource
from app.main.model.message import Message


def __make_users_chat(user1, user2):
    c1 = UsersChat(of_user=user1)
    c2 = UsersChat(of_user=user2)
    c1.other_user_chat = c2
    c2.other_user_chat = c1
    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()

    return c1


def get_user_chats_with_users(user):
    return user.chats_with_users.all(), 200


def get_user_chat_with_user(user, user_id):
    other_user = User.query.filter(User.id == user_id).first_or_404()
    try:
        chat = user.chat_with_user(other_user).one()
        chat.last_opened_on = datetime.utcnow()
        db.session.commit()
        return chat, 200
    except:
        return {}, 300


def send_message_to_user(user, user_id, request):
    other_user = User.query.filter(User.id == user_id).first_or_404()

    try:
        message_body = extract_resource(request, 'body')
    except:
        return {}, 400

    try:
        chat = other_user.chat_with_user(user).one()
    except:
        chat = __make_users_chat(other_user, user)

    new_message = Message(body=message_body, sender_user=user, receiver_chat=chat)

    db.session.add(new_message)
    db.session.commit()

    return new_message, 201
