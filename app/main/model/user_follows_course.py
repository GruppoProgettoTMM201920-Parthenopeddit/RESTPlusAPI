from app.main import db

user_follows_course = db.Table(
    'user_follows_course',
    db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
)