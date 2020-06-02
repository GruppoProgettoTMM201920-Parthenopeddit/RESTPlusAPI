from app.main import db


class Chat(db.Model):
    __tablename__ = "chat"

    # DATA COLUMNS
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # RELATIONSHIPS
    received_messages = db.relationship(
        'Message',
        back_populates='receiver_chat',
        lazy='dynamic',
        cascade="delete"
    )

    # INHERITANCE
    type = db.Column(db.String(255))
    __mapper_args__ = {
        'polymorphic_identity': 'chat',
        'polymorphic_on': type
    }
