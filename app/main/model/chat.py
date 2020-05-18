from datetime import datetime

from app.main import db


class Chat(db.Model):
    __tablename__ = "chat"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    of_group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True, default=None)

    # RELATIONSHIPS
    of_group = db.relationship(
        'Group',
        back_populates='chat'
    )
    received_messages = db.relationship(
        'Message',
        back_populates='receiver_chat',
        lazy='dynamic'
    )

    # INHERITANCE
    type = db.Column(db.Text())
    __mapper_args__ = {
        'polymorphic_identity': 'chat',
        'polymorphic_on': type
    }
