from datetime import datetime, timezone

from app.main import db


class GroupInvite(db.Model):
    inviter_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    invited_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    inviter = db.relationship(
        'User',
        foreign_keys='GroupInvite.inviter_id'
    )
    invited = db.relationship(
        'User',
        foreign_keys='GroupInvite.invited_id'
    )
    group = db.relationship(
        'Group',
        back_populates='invites'
    )
