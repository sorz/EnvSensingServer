from flask import Blueprint, request, jsonify, g

from .. import db
from ..models.measure import MeasurePoint, MeasureValue
from . import auth, get_json_params, APIException


bp = Blueprint("measures", __name__)

@bp.route('/', methods=['GET'])
@auth.login_required
def index():
    # TODO: paging and filter
    pass


@bp.route('/', methods=['POST'])
@auth.login_required
def create():
    device = get_json_params()
    # TODO

