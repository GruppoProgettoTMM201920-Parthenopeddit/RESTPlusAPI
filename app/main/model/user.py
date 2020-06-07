from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app.main import db, whooshee
from app.main.model.course import Course
from app.main.model.group import Group
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

    @hybrid_property
    def published_posts(self):
        return self.published_content.filter(Content.type == 'post')

    @hybrid_property
    def published_reviews(self):
        return self.published_content.filter(Content.type == 'review')

    @hybrid_property
    def published_comments(self):
        return self.published_content.filter(Content.type == 'comment')

    @hybrid_property
    def get_posts_feed(self):
        joined_groups_sq = self.joined_groups.subquery('joined_groups', True)
        followed_courses_sq = self.followed_courses.subquery('followed_courses', True)

        return Post.query.join(
            joined_groups_sq,
            Post.posted_to_board_id == joined_groups_sq.c.group_id
        ).union(
            Post.query.join(
            followed_courses_sq,
            Post.posted_to_board_id == followed_courses_sq.c.course_id
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
