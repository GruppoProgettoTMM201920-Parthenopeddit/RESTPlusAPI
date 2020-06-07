from datetime import datetime

from .. import db


class GroupMember(db.Model):
    __tablename__ = 'group_member'

    user_id = db.Column(db.String(255), db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_chat_read = db.Column(db.DateTime, default=datetime.utcnow)
    is_owner = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship(
        'User',
        back_populates='groups',
        lazy=True
    )
    group = db.relationship(
        'Group',
        back_populates='members',
        lazy=True
    )

