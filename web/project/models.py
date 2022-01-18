from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from project import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tracks = db.relationship('Track', backref='author', lazy='dynamic')
    bio = db.Column(db.String(140), default='')
    color = db.Column(db.String(10))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, username, image=None):
        self.username = username
        self.image = image


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_title = db.Column(db.String(140))
    artist = db.Column(db.String(60))
    album_title = db.Column(db.String(140))
    year = db.Column(db.String(4))
    label = db.Column(db.String(140))
    path = db.Column(db.String())
    channel = db.Column(db.String(2))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<{} by {}. {}: "{}">'.format(
            self.song_title, self.artist, self.year, self.album_title)


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.String)
    color = db.Column(db.String(10))
    link = db.Column(db.String)

    def __repr__(self):
        return '<id: {}, tags: {}>'.format(self.id, self.tags)
