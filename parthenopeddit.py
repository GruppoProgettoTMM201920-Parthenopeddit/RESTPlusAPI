import os

from flask import render_template
from flask_socketio import send

import cli
from app import blueprint
from app.main import create_app, db, socketio

# Importing all model classes to init ORM mapping
from app.main.model.board import Board
from app.main.model.chat import Chat
from app.main.model.comment import Comment
from app.main.model.content import Content
from app.main.model.course import Course
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

# Socket io test
# @app.route("/javascript/socketio")
# def js_socketio():
#     return app.send_static_file("javascript/socketio.js")
#
#
# @app.route("/javascript/jquery")
# def js_query():
#     return app.send_static_file("javascript/jquery.js")
#
#
# @socketio.on('message')
# def handleMessage(msg):
#     print('Message: ' + msg)
#     send(msg, broadcast=True)
#
#
# @app.route('/chatapp')
# def chatapp():
#     return render_template('index.html')
#

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db
    }


if __name__ == '__main__':
    socketio.run(app)
