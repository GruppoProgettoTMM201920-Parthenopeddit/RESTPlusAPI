from datetime import datetime
from app.main import db
from app.main.model.groups_join_users import is_part_of
from app.main.model.dislikes import dislikes
from app.main.model.follows import follows
from app.main.model.likes import likes


class User(db.Model):
    __tablename__ = 'user'

    # DATA COLUMNS
    id = db.Column(db.String, primary_key=True, autoincrement=False)
    nome_visualizzato = db.Column(db.String(32), index=True, unique=True, nullable=True)
    registrato_il = db.Column(db.DateTime, default=datetime.utcnow())

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
        back_populates='following_users',
        lazy='dynamic'
    )
    joined_groups = db.relationship(
        'Group',
        secondary=is_part_of,
        back_populates='member_users',
        lazy='dynamic'
    )

    def __repr__(self) -> str:
        return "<User [{}]>".format(self.id)
