from datetime import datetime, timezone

import sqlalchemy
from sqlalchemy import literal, cast, func, or_
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import query_expression

from app.main import db
from app.main.model.dislikes import Dislikes
from app.main.model.likes import Likes


class Content(db.Model):
    __tablename__ = 'content'

    # DATA COLUMNS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text(4294000000), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

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

    @hybrid_method
    def liked(self, user):
        return db.session.query(
            Content.query.filter(Content.id == self.id).join(Likes).filter(Likes.user_id == user.id).exists()
        ).scalar()

    @hybrid_method
    def disliked(self, user):
        return db.session.query(
            Content.query.filter(Content.id == self.id).join(Dislikes).filter(Dislikes.user_id == user.id).exists()
        ).scalar()

    @staticmethod
    def get_content_with_user_data(content_query, user):
        return content_query.outerjoin(Likes).filter(
            or_(Likes.user_id == user.id, Likes.user_id == None)
        ).outerjoin(Dislikes).filter(
            or_(Dislikes.user_id == user.id, Dislikes.user_id == None)
        ).with_entities(
            Content,
            cast(func.count(Likes.user_id), sqlalchemy.Boolean).label('liked'),
            cast(func.count(Dislikes.user_id), sqlalchemy.Boolean).label('disliked')
        ).group_by(
            Content.id
        )


    # INHERITANCE
    type = db.Column(db.String(255))
    __mapper_args__ = {
        'polymorphic_identity': 'content',
        'polymorphic_on': type
    }
