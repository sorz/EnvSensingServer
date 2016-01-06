from flask import Blueprint, jsonify, g
from flask.ext.login import login_required, current_user


bp = Blueprint("api_token", __name__)

@bp.route('/', methods=['GET'])
@login_required
def get_token():
    return jsonify(token=current_user.generate_token())

