from .board import Board
from .follows import follows
from .. import db


class Course(Board):
    __tablename__ = "course"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key=True)

    # RELATIONSHIPS
    reviews = db.relationship(
        'Review',
        back_populates='reviewed_course',
        lazy='dynamic'
    )
    following_users = db.relationship(
        'User',
        secondary=follows,
        back_populates='followed_courses',
        lazy='dynamic'
    )

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'course',
    }
