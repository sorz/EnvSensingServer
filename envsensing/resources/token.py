from flask import Blueprint, jsonify, g

from . import auth


bp = Blueprint("token", __name__)

@bp.route('/', methods=['GET'])
@auth.login_required
def get_token():
    return jsonify(token=g.user.generate_token())

