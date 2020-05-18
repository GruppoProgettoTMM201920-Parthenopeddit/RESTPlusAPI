from datetime import datetime

from .. import db

is_member = db.Table(
    'is_member',
    db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),

    db.Column('join_date', db.DateTime, default=datetime.utcnow()),
    db.Column('last_opened_chat', db.DateTime, default=datetime.utcnow()),
)
