from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.ext.hybrid import hybrid_property

from app.main import db
from app.main.model.chat import Chat
from app.main.model.message import Message


class UsersChat(Chat):
    __tablename__ = "users_chat"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('chat.id'), primary_key=True, autoincrement=True)
    of_user_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=False)
    last_opened_on = db.Column(db.DateTime, default=datetime.utcnow)
    other_user_chat_id = db.Column(db.Integer, db.ForeignKey('users_chat.id'))

    # RELATIONSHIPS
    of_user = db.relationship(
        'User',
        back_populates='chats_with_users',
        foreign_keys='UsersChat.of_user_id',
    )
    other_user_chat = db.relationship(
        'UsersChat',
        foreign_keys='UsersChat.other_user_chat_id',
        remote_side='[UsersChat.id]',
        post_update=True,
        cascade="delete"
    )

    @hybrid_property
    def sent_messages(self):
        return self.other_user_chat.received_messages

    @hybrid_property
    def last_message(self):
        return self.received_messages.union(
            self.sent_messages
        ).order_by(
            desc(Message.timestamp)
        ).limit(1).one()

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'users_chat',
        'inherit_condition': id == Chat.id,
    }
