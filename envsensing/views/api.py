from flask import Blueprint, request, jsonify

from .. import db
from ..models import User


api = Blueprint("api", __name__)


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


@api.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@api.route('/users', methods=['POST'])
def new_user():
    # Reference:
    # http://blog.miguelgrinberg.com/post/restful-authentication-with-flask
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if username is None or email is None or password is None:
        raise APIException('Lack of arguments.')
    if User.query.filter_by(username=username).first() is not None:
        raise APIException('Username exist.')
    if User.query.filter_by(email=email).first() is not None:
        raise APIException('Email exist.')

    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()
    return '', 204

