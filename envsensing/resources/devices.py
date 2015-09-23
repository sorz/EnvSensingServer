from flask import Blueprint, request, jsonify, g

from .. import db
from ..models.device import Device
from . import auth, get_json_params, APIException


bp = Blueprint("devices", __name__)

@bp.route('/', methods=['GET'])
@auth.login_required
def index():
    records = g.user.devices.all()
    devices = [dict(device_id=r.device_id, name=r.name) for r in records]
    return jsonify(devices=devices)


@bp.route('/<device_id>/', methods=['GET'])
@auth.login_required
def get(device_id):
    device = g.user.devices.filter_by(device_id=device_id).first()
    if device is None:
        raise APIException("Device not found", 404)
    return jsonify(device_id=device.device_id, name=device.name)


@bp.route('/<device_id>/', methods=['PUT'])
@auth.login_required
def update(device_id):
    name = get_json_params()['name']
    device = g.user.devices.filter_by(device_id=device_id).first()
    if device is None:
        device = Device(g.user, device_id, name)
    else:
        device.name = name

    db.session.add(device)
    db.session.commit()
    return '', 204


@bp.route('/<device_id>/', methods=['POST'])
@auth.login_required
def create(device_id):
    device = get_json_params()
    if g.user.devices.filter_by(
            device_id=device_id).first() is not None:
        raise APIException('Device has been registered.')

    device = Device(g.user, device_id, device['name'])
    db.session.add(device)
    db.session.commit()
    return '', 204

