from datetime import datetime

from app.main import db
from app.main.model.board import Board
from app.main.model.dislikes import dislikes
from app.main.model.is_member import is_member
from app.main.model.likes import likes
from app.main.model.post import Post


class User(db.Model):
    __tablename__ = 'user'

    # DATA COLUMNS
    id = db.Column(db.String, primary_key=True, autoincrement=False)
    display_name = db.Column(db.String(32), index=True, unique=True, nullable=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow())

    # RELATIONSHIPS
    published_content = db.relationship(
        'Content',
        back_populates='author',
        lazy='dynamic'
    )
    liked_content = db.relationship(
        'Content',
        secondary=likes,
        back_populates='liked_by_users',
        lazy='dynamic'
    )
    disliked_content = db.relationship(
        'Content',
        secondary=dislikes,
        back_populates='disliked_by_users',
        lazy='dynamic'
    )
    boards = db.relationship(
        'Board',
        secondary=is_member,
        back_populates='members',
        lazy='dynamic'
    )

    def get_visible_posts(self):
        return Post.query.filter(
            Post.posted_to_board_id.in_(
                self.boards.with_entities(Board.id)
            )
        ).union(
            Post.query.filter(Post.posted_to_board_id == None)
        )
