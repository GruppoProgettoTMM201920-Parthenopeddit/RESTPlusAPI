from .. import db


dislikes = db.Table(
    'dislikes',
    db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
    db.Column('content_id', db.Integer, db.ForeignKey('content.id'), primary_key=True)
)
