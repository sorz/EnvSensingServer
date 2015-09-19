from flask import Blueprint, request, jsonify, g
from flask.ext.httpauth import HTTPBasicAuth

from .. import db
from ..models.user import User
from . import APIException


bp = Blueprint("user", __name__)
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


@bp.route('/users', methods=['POST'])
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


@bp.route('/token', methods=['GET'])
@auth.login_required
def get_token():
    return jsonify({ 'token': g.user.generate_token() })

