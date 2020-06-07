from datetime import datetime

from sqlalchemy import literal
from sqlalchemy.ext.hybrid import hybrid_property

from app.main import db, whooshee
from app.main.model.course import Course
from app.main.model.dislikes import Dislikes
from app.main.model.group import Group
from app.main.model.likes import Likes
from app.main.model.post import Post
from app.main.model.user_follows_course import user_follows_course


@whooshee.register_model('id', 'display_name')
class User(db.Model):
    __tablename__ = 'user'

    # DATA COLUMNS
    id = db.Column(db.String(255), primary_key=True, autoincrement=False)
    display_name = db.Column(db.String(255), unique=True, nullable=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    # RELATIONSHIPS
    published_content = db.relationship(
        'Content',
        back_populates='author',
        lazy='dynamic'
    )
    liked_content = db.relationship(
        'Likes',
        back_populates='user',
        lazy='dynamic'
    )
    disliked_content = db.relationship(
        'Dislikes',
        back_populates='user',
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

    # def get_courses_with_followed_flag(self):
    #     return Course.query.join(User.followed_courses).filter(User.id == self.id).with_entities(
    #         Course, literal(True).label('followed')
    #     ).union(
    #         Course.query.outerjoin(User.followed_courses).filter(User.id != self.id).with_entities(
    #             Course, literal(False).label('followed')
    #         )
    #     ).all()
