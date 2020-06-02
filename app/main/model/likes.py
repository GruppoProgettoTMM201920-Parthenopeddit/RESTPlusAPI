from .. import db


class Likes(db.Model):
    __tablename__ = 'likes'

    # DATA COLUMNS
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True)

    user = db.relationship(
        'User',
        back_populates='liked_content',
        lazy=True,
    )
    content = db.relationship(
        'Content',
        back_populates='likes',
        lazy=True,
    )
