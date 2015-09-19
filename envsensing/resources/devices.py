from flask import Blueprint, request, jsonify, g

from .. import db
from ..models.device import Device
from . import APIException


bp = Blueprint("devices", __name__)

@bp.route('/devices', methods=['GET', 'POST'])
def new_user():
    pass
