from statistics import mean

from sqlalchemy import select, func
from sqlalchemy.ext.hybrid import hybrid_property

from .board import Board
from .follows import follows
from .review import Review
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
    followers = db.relationship(
        'User',
        secondary=follows,
        back_populates='followed_courses',
        lazy='dynamic'
    )

    # AGGREGATED COLUMNS
    @hybrid_property
    def followers_num(self):
        return self.followers.count()

    @hybrid_property
    def reviews_count(self):
        return self.reviews.count()

    @hybrid_property
    def average_difficulty_score(self):
        return mean(rev.score_difficulty for rev in self.reviews)

    @average_difficulty_score.expression
    def average_difficulty_score(cls):
        return select([func.avg(Review.score_difficulty)]). \
            where(Review.reviewed_course_id == cls.id). \
            label('average_difficulty_score')

    @hybrid_property
    def average_liking_score(self):
        return mean(rev.score_liking for rev in self.reviews)

    @average_liking_score.expression
    def average_liking_score(cls):
        return select([func.avg(Review.score_liking)]). \
            where(Review.reviewed_course_id == cls.id). \
            label('average_liking_score')

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'course',
    }
