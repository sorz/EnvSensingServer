from flask import Blueprint, request, jsonify, g

from .. import db
from ..models.user import User
from . import get_json_params, APIException


bp = Blueprint("api_users", __name__)

@bp.route('/', methods=['POST'])
def new_user():
    user = get_json_params()

    if User.query.filter_by(username=user['username']).first() is not None:
        raise APIException('Username exist, please try another one or login.')
    if User.query.filter_by(email=user['email']).first() is not None:
        raise APIException('Email exist, please try another one or login.')

    user = User(user['username'], user['email'], user['password'])
    db.session.add(user)
    db.session.commit()
    return '', 204

