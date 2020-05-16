from .content import Content
from .. import db


class Comment(Content):
    __tablename__ = "comment"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True)

    # FOREIGN KEYS COLUMNS
    commented_content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)

    # RELATIONSHIPS
    commented_content = db.relationship(
        'Content',
        back_populates='comments',
        lazy=True,
        foreign_keys='Comment.commented_content_id'
    )

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'comment',
        'inherit_condition': id == Content.id,
    }
