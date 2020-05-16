from .content import Content
from .. import db


class Post(Content):
    __tablename__ = "post"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'post',
    }
