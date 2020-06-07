from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from app.main.model.board import Board
from app.main import db


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

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }
