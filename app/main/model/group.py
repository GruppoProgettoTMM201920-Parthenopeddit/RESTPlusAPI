from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property


from .board import Board

from .is_member import is_member
from .. import db


class Group(Board):
    __tablename__ = "group"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())

    # RELATIONSHIPS
    members = db.relationship(
        'User',
        secondary=is_member,
        back_populates='joined_groups',
        lazy='dynamic'
    )
    chat = db.relationship(
        'GroupChat',
        back_populates='of_group'
    )

    # AGGREGATED COLUMNS
    @hybrid_property
    def members_num(self):
        return self.members.count()

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }
