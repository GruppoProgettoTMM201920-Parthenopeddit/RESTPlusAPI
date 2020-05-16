from datetime import datetime

from app.main import db


class User(db.Model):
    __tablename__ = 'user'

    # DATA COLUMNS
    id = db.Column(db.String, primary_key=True, autoincrement=False)
    nome_visualizzato = db.Column(db.String(32), index=True, unique=True, nullable=True)
    registrato_il = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # RELATIONSHIPS
    published_content = db.relationship(
        'Content',
        back_populates='author',
        lazy='dynamic'
    )
