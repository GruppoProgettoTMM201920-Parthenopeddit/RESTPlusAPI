from sqlalchemy.ext.hybrid import hybrid_property

from app.main import db


class Board(db.Model):
    __tablename__ = 'board'

    # DATA COLUMNS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, nullable=False)

    # RELATIONSHIPS
    posts = db.relationship(
        'Post',
        back_populates='posted_to_board',
        lazy='dynamic',
        cascade="delete"
    )

    # AGGREGATED COLUMNS
    @hybrid_property
    def posts_num(self):
        return self.posts.count()

    # INHERITANCE
    type = db.Column(db.Text())
    __mapper_args__ = {
        'polymorphic_identity': 'board',
        'polymorphic_on': type
    }
