from datetime import datetime, timezone

from .. import db


class GroupMember(db.Model):
    __tablename__ = 'group_member'

    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    join_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_chat_read = db.Column(db.DateTime, nullable=True)
    is_owner = db.Column(db.Boolean, nullable=False)

    user = db.relationship(
        'User',
        back_populates='groups'
    )
    group = db.relationship(
        'Group',
        back_populates='members',
    )
