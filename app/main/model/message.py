from datetime import datetime

from app.main import db


class Message(db.Model):
    __tablename__ = "message"

    # DATA COLUMNS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text(4294000000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    replies_to_message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=True)

    # FOREIGN KEYS COLUMNS
    sender_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)

    # RELATIONSHIPS
    sender_user = db.relationship(
        'User',
        back_populates='sent_messages',
        lazy=True
    )
    receiver_chat = db.relationship(
        'Chat',
        back_populates='received_messages',
        lazy=True
    )
    replies_to_message = db.relationship(
        'Message',
        remote_side='[Message.id]'
    )
