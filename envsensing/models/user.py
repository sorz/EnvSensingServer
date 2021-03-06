from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from sqlalchemy.ext.hybrid import hybrid_property
from base64 import b64decode

from .. import app, db, bcrypt, login_manager


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(90), unique=True)
    password_hash = db.Column(db.String(128))

    devices = db.relationship('Device', backref='user', lazy='dynamic')


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


    def get_id(self):
        """Required by Flask-Login."""
        return str(self.id)


    @hybrid_property
    def is_authenticated(self):
        """Required by Flask-User."""
        # All users in database are authenticated.
        return True


    @hybrid_property
    def is_active(self):
        """Required by Flask-User."""
        # All users in database are actived.
        return True


    @hybrid_property
    def is_anonymous(self):
        """Required by Flask-User."""
        # Not users in database are anonymous.
        return False


    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    """Flask-User's callback function,
    used to reload the user object from the user ID stored in the session.
    """
    return User.query.get(user_id)


@login_manager.request_loader
def load_user_from_request(request):
    """Add basic auth for API call."""
    auth = request.headers.get('Authorization')
    if auth is not None:
        auth = auth.replace('Basic ', '', 1)
        try:
            token_or_username, password = b64decode(auth).decode().split(':', 1)
        except TypeError:
            return

        # Treat it as token first. If fail, try username & password auth.
        user = User.verify_token(token_or_username)
        if user is not None:
            request.with_basic_auth = True
            return user
        else:
            user = User.query.filter_by(username=token_or_username).first()
            if user.verify_password(password):
                request.with_basic_auth = True
                return user

