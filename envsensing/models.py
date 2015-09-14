from sqlalchemy.ext.hybrid import hybrid_property

from . import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(90), unique=True)
    password_hash = db.Column(db.String(128))


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


    @hybrid_property
    def password(self):
        return self.password_hash


    @password.setter
    def _set_password(self, plaintext):
        self.password_hash = bcrypt.generate_password_hash(plaintext)


    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password_hash, plaintext)


    def __repr__(self):
        return '<User %r>' % self.username

