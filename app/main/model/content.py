from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from .likes import likes
from .. import db


class Content(db.Model):
    __tablename__ = 'content'

    # DATA COLUMNS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    # FOREIGN KEYS COLUMNS
    author_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    # RELATIONSHIPS
    # author [ backref of User -> published_content ]
    comments = db.relationship(
        'Comment',
        backref='commented_content',
        lazy='dynamic',
        foreign_keys='Comment.commented_content_id'
    )
    liked_by_users = db.relationship(
        'User',
        secondary=likes,
        back_populates='liked_content',
        lazy='dynamic'
    )

    # AGGREGATED COLUMNS
    @hybrid_property
    def comments_num(self):
        sum = self.comments.count()
        if sum > 0:
            for content in self.comments.all():
                sum += content.comments_num
        return sum

    # INHERITANCE
    type = db.Column(db.Text())
    __mapper_args__ = {
        'polymorphic_identity': 'content',
        'polymorphic_on': type
    }
