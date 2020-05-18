from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from .dislikes import dislikes
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
    author = db.relationship(
        'User',
        back_populates='published_content',
        lazy=True
    )
    comments = db.relationship(
        'Comment',
        back_populates='commented_content',
        lazy='dynamic',
        foreign_keys='Comment.commented_content_id'
    )
    liked_by_users = db.relationship(
        'User',
        secondary=likes,
        back_populates='liked_content',
        lazy='dynamic'
    )
    disliked_by_users = db.relationship(
        'User',
        secondary=dislikes,
        back_populates='disliked_content',
        lazy='dynamic'
    )

    # AGGREGATED COLUMNS
    @hybrid_property
    def author_display_name(self):
        return self.author.display_name

    @hybrid_property
    def comments_num(self):
        sum = self.comments.count()
        if sum > 0:
            for content in self.comments.all():
                sum += content.comments_num
        return sum

    @hybrid_property
    def likes_num(self):
        return self.likes.count()

    @hybrid_property
    def dislikes_num(self):
        return self.dislikes.count()

    # INHERITANCE
    type = db.Column(db.Text())
    __mapper_args__ = {
        'polymorphic_identity': 'content',
        'polymorphic_on': type
    }
