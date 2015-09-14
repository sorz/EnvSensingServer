from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from sqlalchemy.ext.hybrid import hybrid_property

from .. import app, db, bcrypt


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


    def verify_password(self, plaintext):
        return bcrypt.check_password_hash(self.password_hash, plaintext)


    def generate_token(self):
        # Reference:
        # http://blog.miguelgrinberg.com/post/restful-authentication-with-flask
        expiration = app.config.get('AUTH_TOKEN_EXPIRATION', 24 * 3600)
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id}).decode()


    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (SignatureExpired, BadSignature):
            return
        return User.query.get(data['id'])


    def __repr__(self):
        return '<User %r>' % self.username

