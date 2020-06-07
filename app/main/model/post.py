from app.main import db, whooshee
from app.main.model.content import Content


@whooshee.register_model('title')
class Post(Content):
    __tablename__ = "post"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True)
    title = db.Column(db.String(1024), nullable=False)

    # FOREIGN KEYS COLUMNS
    posted_to_board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=True)

    # RELATIONSHIPS
    posted_to_board = db.relationship(
        'Board',
        back_populates='posts',
        lazy=True
    )

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'post',
    }
