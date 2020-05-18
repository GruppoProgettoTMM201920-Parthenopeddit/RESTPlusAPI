from datetime import datetime

from app.main import db
from app.main.model.chat import Chat


class Friendship(Chat):
    __tablename__ = "friendship"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('chat.id'), primary_key=True)
    sent_on = db.Column(db.DateTime, default=datetime.utcnow())
    accepted = db.Column(db.Boolean)
    accepted_on = db.Column(db.DateTime, default=datetime.utcnow())

    sending_user_last_opened_chat = db.Column(db.DateTime, default=datetime.utcnow())
    receiving_user_last_opened_chat = db.Column(db.DateTime, default=datetime.utcnow())

    # FOREIGN KEYS COLUMNS
    sending_user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    receiving_user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    # RELATIONSHIPS
    sending_user = db.relationship(
        'User',
        back_populates='sent_friendships',
        lazy=True,
        foreign_keys=[sending_user_id]
    )
    receiving_user = db.relationship(
        'User',
        back_populates='received_friendships',
        lazy=True,
        foreign_keys=[receiving_user_id]
    )

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'friendship'
    }
