from app import db
from flask_login import UserMixin
from hashlib import md5
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False)
    password = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(120), unique=True)
    job = db.Column(db.String(12))
    activate = db.Column(db.Boolean, default=False)
    retrieve = db.Column(db.Boolean, default=False)
    books = db.relationship('Book', backref='owner', lazy='dynamic')
    about_me = db.Column(db.String(140))
    #last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.name)

    def avatar(self, size):
        return 'https://s.gravatar.com/avatar/3655d460a7a9817d6daf931933b4c0b1?s=80' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    info = db.Column(db.String(80))
    url = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<Book %r>' % (self.title)
