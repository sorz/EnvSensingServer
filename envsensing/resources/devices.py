from flask import Blueprint, request, jsonify, g
from flask.ext.login import login_required, current_user

from .. import db
from ..models.device import Device
from . import get_json_params, APIException


bp = Blueprint("api_devices", __name__)

@bp.route('/', methods=['GET'])
@login_required
def index():
    records = current_user.devices.all()
    devices = [dict(device_id=r.device_id, name=r.name) for r in records]
    return jsonify(devices=devices)


@bp.route('/<device_id>/', methods=['GET'])
@login_required
def get(device_id):
    device = current_user.devices.filter_by(device_id=device_id).first()
    if device is None:
        raise APIException("Device not found", 404)
    return jsonify(device_id=device.device_id, name=device.name)


@bp.route('/<device_id>/', methods=['PUT'])
@login_required
def update(device_id):
    name = get_json_params()['name']
    device = current_user.devices.filter_by(device_id=device_id).first()
    if device is None:
        device = Device(current_user, device_id, name)
    else:
        device.name = name

    db.session.add(device)
    db.session.commit()
    return '', 204


@bp.route('/<device_id>/', methods=['POST'])
@login_required
def create(device_id):
    device = get_json_params()
    if current_user.devices.filter_by(
            device_id=device_id).first() is not None:
        raise APIException('Device has been registered.')

    device = Device(current_user, device_id, device['name'])
    db.session.add(device)
    db.session.commit()
    return '', 204

