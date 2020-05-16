from .content import Content
from .. import db


class Review(Content):
    __tablename__ = "review"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True)
    score_liking = db.Column(db.Integer, nullable=True)
    score_difficulty = db.Column(db.Integer, nullable=True)

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'review',
    }
