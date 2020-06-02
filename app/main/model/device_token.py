from app.main import db


class DeviceToken(db.Model):
    __tablename__ = "device_token"

    # DATA COLUMNS
    token = db.Column(db.String(1024), primary_key=True, autoincrement=False)

    # FOREIGN KEYS COLUMNS
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=False)

    # RELATIONSHIPS
    user = db.relationship(
        'User',
        back_populates='devices_tokens',
        lazy=True
    )
