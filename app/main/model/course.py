from statistics import mean

from sqlalchemy import select, func
from sqlalchemy.ext.hybrid import hybrid_property

from .board import Board
from .review import Review
from .user_follows_course import user_follows_course
from app.main import db


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
        secondary=user_follows_course,
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
        return Review.query.with_entities(
            func.avg(Review.score_difficulty)
                .label('average_difficulty_score')
        ).filter(
            Review.reviewed_course_id == self.id
        ).scalar()

    @hybrid_property
    def average_liking_score(self):
        return Review.query.with_entities(
            func.avg(Review.score_liking)
                .label('average_liking_score')
        ).filter(
            Review.reviewed_course_id == self.id
        ).scalar()

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'course',
    }
