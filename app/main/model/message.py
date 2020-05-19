from datetime import datetime

from app.main import db


class Message(db.Model):
    __tablename__ = "message"

    # DATA COLUMNS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    replies_to_message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=True)

    # FOREIGN KEYS COLUMNS
    sender_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.String, db.ForeignKey('chat.id'), nullable=False)

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

    # TODO ADD SELF REFERENCING RELATIONSHIP AND HYBRID DATA TO OTHER CLASSES
