from sqlalchemy.ext.hybrid import hybrid_property

from .board import Board
from .groups_join_users import is_part_of
from .. import db


class Group(Board):
    __tablename__ = "group"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key=True)

    # RELATIONSHIPS
    members = db.relationship(
        'User',
        secondary=is_part_of,
        back_populates='joined_groups',
        lazy='dynamic'
    )

    # AGGREGATED COLUMNS
    @hybrid_property
    def members_num(self):
        return self.members.count()

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }
