from datetime import datetime

from .. import db

is_member = db.Table(
    'is_member',
    db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
    db.Column('board_id', db.Integer, db.ForeignKey('board.id'), primary_key=True),

    db.Column('join_date', db.DateTime, default=datetime.utcnow()),
)
