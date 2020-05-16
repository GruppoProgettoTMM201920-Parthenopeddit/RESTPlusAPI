from datetime import datetime
from .. import db


class Content(db.Model.__base__):
    __tablename__ = 'content'

    # DATA COLUMNS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    # FOREIGN KEYS COLUMNS
    author_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    # RELATIONSHIPS
    author = db.relationship(
        'User',
        back_populates='published_content',
        lazy='dynamic'
    )
    comments = db.relationship(
        'Comment',
    )

    # INHERITANCE
    type = db.Column(db.Text())
    __mapper_args__ = {
        'polymorphic_identity': 'content',
        'polymorphic_on': type
    }
