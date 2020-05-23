from app.main import db
from app.main.model.chat import Chat


class UsersChat(Chat):
    __tablename__ = "users_chat"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('chat.id'), primary_key=True, autoincrement=True)
    of_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_opened_on = db.Column(db.DateTime, nullable=True)
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

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'users_chat',
        'inherit_condition': id == Chat.id,
    }
