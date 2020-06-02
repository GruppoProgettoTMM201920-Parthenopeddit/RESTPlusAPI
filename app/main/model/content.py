from datetime import datetime, timezone

from sqlalchemy.ext.hybrid import hybrid_property

from app.main.model.dislikes import Dislikes
from app.main.model.likes import Likes
from .. import db


class Content(db.Model):
    __tablename__ = 'content'

    # DATA COLUMNS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text(4294000000), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))

    # FOREIGN KEYS COLUMNS
    author_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=False)

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
        foreign_keys='Comment.commented_content_id',
        cascade="delete"
    )
    likes = db.relationship(
        'Likes',
        back_populates='content',
        lazy='dynamic',
        cascade="delete"
    )
    dislikes = db.relationship(
        'Dislikes',
        back_populates='content',
        lazy='dynamic',
        cascade="delete"
    )

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
    type = db.Column(db.String(255))
    __mapper_args__ = {
        'polymorphic_identity': 'content',
        'polymorphic_on': type
    }
