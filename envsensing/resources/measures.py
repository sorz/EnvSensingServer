from functools import wraps
from flask import Blueprint, request, jsonify, g
from flask.ext.login import login_required, current_user
from datetime import datetime, timedelta

from .. import db
from ..models.device import Device
from ..models.measure import MeasurePoint, MeasureValue
from . import csrf_protect, get_json_params, APIException


bp = Blueprint("api_measures", __name__)

def device_context(f):
    # Reference:
    # http://flask.pocoo.org/docs/0.10/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        device_id = kwargs.pop('device_id')
        g.device = current_user.devices.filter_by(device_id=device_id).first()
        if g.device is None:
            raise APIException('Device not found.', 404)
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/', methods=['GET'])
@login_required
@device_context
def index():
    try:
        date_from = datetime.strptime(request.args.get('from'), '%Y-%m-%d')
    except ValueError:
        date_from = None
    try:
        date_to = datetime.strptime(request.args.get('to'), '%Y-%m-%d')
        date_to += timedelta(days=1)
    except ValueError:
        date_to = None

    points = g.device.measure_points.filter()
    if date_from is not None:
        points = points.filter(MeasurePoint.timestamp >= date_from)
    if date_to is not None:
        points = points.filter(MeasurePoint.timestamp < date_to)

    measures = []
    for p in points:
        item = dict(timestamp=p.timestamp.timestamp(),
                    latitude=p.latitude, longitude=p.longitude,
                    accuracy=p.accuracy, values=[])
        for value in p.values.all():
            item['values'].append(dict(type=value.type_name, value=value.value))
        measures.append(item)
    return jsonify(device_id=g.device.device_id, measures=measures)


@bp.route('/', methods=['POST'])
@login_required
@csrf_protect
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
            # Use merge() instead of add() to eliminate duplication.
            # Reference:
            # http://docs.sqlalchemy.org/en/rel_0_9/orm/
            # session_state_management.html#merging
            db.session.merge(point)
            for sensor_type, value in m['values'].items():
                db.session.merge(MeasureValue(point, sensor_type, value))
    except KeyError as e:
        raise APIException('JSON format error: %s not found.' % e)
    except ValueError as e:
        raise APIException(e)

    db.session.commit()
    return '', 204

