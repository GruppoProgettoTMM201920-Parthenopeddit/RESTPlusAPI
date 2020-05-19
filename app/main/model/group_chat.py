from app.main import db
from app.main.model.chat import Chat


class GroupChat(Chat):
    __tablename__ = "group_chat"

    # DATA COLUMNS
    id = db.Column(db.Integer, db.ForeignKey('chat.id'), primary_key=True, autoincrement=True)
    of_group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    # RELATIONSHIPS
    of_group = db.relationship(
        'Group',
        back_populates='chat'
    )

    # INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'group_chat',
    }
