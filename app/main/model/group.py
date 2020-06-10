from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from app.main import db
from app.main.model.board import Board


class Group(Board):
    __tablename__ = "group"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    # RELATIONSHIPS
    chat = db.relationship(
        'GroupChat',
        back_populates='of_group',
        uselist=False,
        cascade="save-update, delete"
    )
    members = db.relationship(
        'GroupMember',
        back_populates='group',
        lazy='dynamic',
        cascade="delete"
    )
    invites = db.relationship(
        'GroupInvite',
        back_populates='group',
        lazy='dynamic',
        cascade="delete"
    )

    # AGGREGATED COLUMNS
    @hybrid_property
    def members_num(self):
        return self.members.count()

    @hybrid_property
    def involved_users(self):
        from app.main.model.user import User
        from app.main.model.group_invite import GroupInvite

        return self.members.join(User).with_entities(User).union(
            self.invites.join(User, User.id == GroupInvite.invited_id).with_entities(User)
        )

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }
