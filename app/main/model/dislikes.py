from .. import db


class Dislikes(db.Model):
    __tablename__ = "dislikes"

    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True)
