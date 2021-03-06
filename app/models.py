import jwt
from time import time
from app import db, login
from flask import current_app
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_verified = db.Column(db.Boolean, unique=False, default=False)
    files = db.relationship('File', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_email_token(self, expires_in=600):
        return jwt.encode(
            {'email_id': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_email_token(token):
        try:
            jwt_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                                algorithms=['HS256'])['email_id']
        except:
            return False

        return jwt_id

    def __repr__(self):
        return '<User {}>'.format(self.username)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    key = db.Column(db.String(64), index=True)
    body = db.Column(db.String(140))
    date = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<File {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
