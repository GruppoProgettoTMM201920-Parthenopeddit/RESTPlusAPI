from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from app.main import db
from app.main.model.board import Board
from app.main.model.course import Course
from app.main.model.dislikes import dislikes
from app.main.model.follows import follows
from app.main.model.group import Group
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
    followed_courses = db.relationship(
        'Course',
        secondary=follows,
        back_populates='followers',
        lazy='dynamic'
    )
    joined_groups = db.relationship(
        'Group',
        secondary=is_member,
        back_populates='members',
        lazy='dynamic'
    )
    sent_friendships = db.relationship(
        'Friendship',
        back_populates='sending_user',
        lazy='dynamic',
        foreign_keys='Friendship.sending_user_id'
    )
    received_friendships = db.relationship(
        'Friendship',
        back_populates='receiving_user',
        lazy='dynamic',
        foreign_keys='Friendship.receiving_user_id'
    )
    sent_messages = db.relationship(
        'Message',
        back_populates='sender_user',
        lazy='dynamic'
    )

    def get_posts_feed(self):
        return Post.query.filter(
            Post.posted_to_board_id.in_(
                self.joined_groups.with_entities(Group.id).union(
                    self.followed_courses.with_entities(Course.id)
                )
            )
        ).union(
            Post.query.filter(
                Post.posted_to_board_id == None
            )
        )
