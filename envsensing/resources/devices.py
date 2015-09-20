from flask import Blueprint, request, jsonify, g

from .. import db
from ..models.device import Device
from . import auth, APIException


bp = Blueprint("devices", __name__)

@bp.route('/devices', methods=['GET'])
@auth.login_required
def index():
    records = g.user.devices.all()
    devices = [dict(device_id=r.device_id, name=r.name) for r in records]
    return jsonify(devices=devices)


@bp.route('/devices/<device_id>', methods=['GET'])
@auth.login_required
def get(device_id):
    device = g.user.devices.filter_by(device_id=device_id).first()
    if device is None:
        raise APIException("Device not found", 404)
    return jsonify(device_id=device.device_id, name=device.name)


@bp.route('/devices/<device_id>', methods=['PUT'])
@auth.login_required
def update(device_id):
    device = g.user.devices.filter_by(device_id=device_id).first()
    if device is None:
        raise APIException("Device not found", 404)
    name = request.form.get('name')
    if name is None:
        raise APIException('Lack of arguments: name')

    device.name = name
    db.session.add(device)
    db.session.commit()
    return '', 204


@bp.route('/devices', methods=['POST'])
@auth.login_required
def create():
    id = request.form.get('device_id')
    name = request.form.get('name')

    if id is None or name is None:
        raise APIException('Lack of arguments.')
    if g.user.devices.filter_by(device_id=id).first() is not None:
        raise APIException('Device has been registered.')

    device = Device(g.user, id, name)
    db.session.add(device)
    db.session.commit()
    return '', 204

