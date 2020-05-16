from .board import Board
from .groups_join_users import is_part_of
from .. import db


class Group(Board):
    __tablename__ = "group"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key=True)

    # RELATIONSHIPS
    member_users = db.relationship(
        'User',
        secondary=is_part_of,
        back_populates='joined_groups',
        lazy='dynamic'
    )

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }
