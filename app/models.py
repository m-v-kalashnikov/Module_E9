from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String)
    events = db.relationship('Event', backref='user', lazy=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetime_start = db.Column(db.DateTime(), unique=False, nullable=True)
    datetime_end = db.Column(db.DateTime(), unique=False, nullable=True)
    topic = db.Column(db.String(50), unique=False, nullable=True)
    description = db.Column(db.String(300), unique=False, nullable=True)

    def get_username(self):
        user = User.query.filter_by(id=self.user_id).first_or_404()
        return user.username
