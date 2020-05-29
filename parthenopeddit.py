import os
import cli
from app import blueprint
from app.main import create_app, db, socketio, fcm

# Importing all model classes to init ORM mapping
from app.main.model.board import Board
from app.main.model.chat import Chat
from app.main.model.comment import Comment
from app.main.model.content import Content
from app.main.model.course import Course
from app.main.model.device_token import DeviceToken
from app.main.model.group import Group
from app.main.model.group_chat import GroupChat
from app.main.model.group_invite import GroupInvite
from app.main.model.group_member import GroupMember
from app.main.model.message import Message
from app.main.model.post import Post
from app.main.model.review import Review
from app.main.model.user import User
from app.main.model.users_chat import UsersChat

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.register_blueprint(blueprint)
app.app_context().push()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db
    }


if __name__ == '__main__':
    socketio.run(app)
