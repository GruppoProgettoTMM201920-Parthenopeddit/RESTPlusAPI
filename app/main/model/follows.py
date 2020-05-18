from app.main import db

follows = db.Table(
    'follows',
    db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
)