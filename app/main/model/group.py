from .board import Board
from .. import db


class Group(Board):
    __tablename__ = "group"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key=True)

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }
