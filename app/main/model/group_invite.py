from datetime import datetime

from app.main import db


class GroupInvite(db.Model):
    __tablename__ = 'group_invite'

    inviter_id = db.Column(db.String(255), db.ForeignKey('user.id'), primary_key=True)
    invited_id = db.Column(db.String(255), db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    inviter = db.relationship(
        'User',
        foreign_keys='GroupInvite.inviter_id'
    )
    invited = db.relationship(
        'User',
        foreign_keys='GroupInvite.invited_id',
        back_populates='group_invites'
    )
    group = db.relationship(
        'Group',
        back_populates='invites'
    )
