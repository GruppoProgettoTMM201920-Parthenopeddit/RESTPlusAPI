from datetime import datetime, timezone

from sqlalchemy.ext.hybrid import hybrid_property

from app.main import db
from app.main.model.course import Course
from app.main.model.dislikes import dislikes
from app.main.model.group import Group
from app.main.model.likes import likes
from app.main.model.post import Post
from app.main.model.user_follows_course import user_follows_course


class User(db.Model):
    __tablename__ = 'user'

    # DATA COLUMNS
    id = db.Column(db.String, primary_key=True, autoincrement=False)
    display_name = db.Column(db.String(32), index=True, unique=True, nullable=True)
    registered_on = db.Column(db.DateTime, default=datetime.now(timezone.utc))

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
        secondary=user_follows_course,
        back_populates='followers',
        lazy='dynamic'
    )
    groups = db.relationship(
        'GroupMember',
        back_populates='user',
        lazy='dynamic'
    )
    sent_messages = db.relationship(
        'Message',
        back_populates='sender_user',
        lazy='dynamic'
    )
    chats_with_users = db.relationship(
        'UsersChat',
        back_populates='of_user',
        foreign_keys='UsersChat.of_user_id',
        lazy='dynamic'
    )
    group_invites = db.relationship(
        'GroupInvite',
        foreign_keys='GroupInvite.invited_id',
        back_populates='invited',
        lazy='dynamic'
    )
    devices_tokens = db.relationship(
        'DeviceToken',
        back_populates='user',
        lazy='dynamic'
    )

    @hybrid_property
    def joined_groups(self):
        return self.groups.join(Group).with_entities(Group)

    # QUERY
    def get_posts_feed(self):
        return Post.query.filter(
            Post.posted_to_board_id.in_(
                self.groups.with_entities(Group.id).union(
                    self.followed_courses.with_entities(Course.id)
                )
            )
        ).union(
            Post.query.filter(
                Post.posted_to_board_id == None
            )
        )
