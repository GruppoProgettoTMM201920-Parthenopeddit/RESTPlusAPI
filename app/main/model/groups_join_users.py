from .. import db


is_part_of = db.Table(
    'is_part_of',
    db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)
