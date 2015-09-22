from functools import wraps
from flask import Blueprint, request, jsonify, g

from .. import db
from ..models.device import Device
from ..models.measure import MeasurePoint, MeasureValue
from . import auth, get_json_params, APIException


bp = Blueprint("measures", __name__)

def device_context(f):
    # Reference:
    # http://flask.pocoo.org/docs/0.10/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        device_id = kwargs.pop('device_id')
        g.device = g.user.devices.filter_by(device_id=device_id).first()
        if g.device is None:
            raise APIException('Device not found.', 404)
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/', methods=['GET'])
@auth.login_required
@device_context
def index():
    raise APIException('Not yet implemented.')


@bp.route('/', methods=['POST'])
@auth.login_required
@device_context
def create():
    measures = request.get_json()
    if measures is None:
        raise APIException('JSON data is required.')

    # Single measure in one request is also allowed.
    if isinstance(measures, dict):
        measures = [measures]

    try:
        for m in measures:
            point = MeasurePoint(g.device, m['timestamp'], m['longitude'],
                                 m['latitude'], m['accuracy'])
            db.session.add(point)
            # TODO: measure values

    except KeyError as e:
        raise APIException('JSON format error: %s not found.' % e)

    #db.session.commit()
    return '', 204
