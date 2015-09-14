from flask import Blueprint, request, jsonify, g
from flask.ext.httpauth import HTTPBasicAuth

from .. import db
from ..models.user import User


api = Blueprint("api", __name__)
auth = HTTPBasicAuth()

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


@auth.verify_password
def verify_password(username, password):
    # Reference:
    # http://blog.miguelgrinberg.com/post/restful-authentication-with-flask
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@api.route('/users', methods=['POST'])
def new_user():
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


@api.route('/token', methods=['GET'])
@auth.login_required
def get_token():
    return jsonify({ 'token': 'TODO' })

