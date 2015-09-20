from flask import g, jsonify
from flask.ext.httpauth import HTTPBasicAuth

from .. import app
from ..models.user import User


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    # Reference:
    # http://blog.miguelgrinberg.com/post/restful-authentication-with-flask
    user = User.verify_token(username_or_token)
    if user is None:
        user = User.query.filter_by(username=username_or_token).first()
        if user is None or not user.verify_password(password):
            return False
    g.user = user
    return True


class APIException(Exception):
    # Reference:
    # http://flask.pocoo.org/docs/0.10/patterns/apierrors/
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

