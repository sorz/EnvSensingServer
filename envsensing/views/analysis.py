from flask import Blueprint, render_template, redirect, url_for, request, \
        flash, jsonify
from flask.ext.login import login_required, login_user, logout_user, \
        current_user
from datetime import datetime, timedelta
from sklearn.metrics import silhouette_score
from sklearn.cluster import MiniBatchKMeans as KMeans
import numpy as np

from .. import db
from ..models.user import User
from ..models.device import Device
from ..models.measure import MeasurePoint, MeasureValue, SENSOR_NAMES


bp = Blueprint("analysis", __name__)


@bp.route('/')
def index():
    return render_template('analysis/index.html')


@bp.route('/status/')
def status():
    context = {}
    context['total_users'] = User.query.count()
    context['total_devices'] = Device.query.count()
    context['total_measures'] = MeasurePoint.query.count()

    return render_template('analysis/status.html', **context)

@bp.route('/maps/')
def maps():
    return render_template('analysis/maps.html')


def _point_to_json_dict(point):
    item = dict(timestamp=point.timestamp.timestamp(),
                deviceId=point.device_id,
                latitude=point.latitude, longitude=point.longitude,
                accuracy=point.accuracy, values=[])
    for value in point.values.all():
        item['values'].append(dict(type=value.type_name, value=value.value))
    return item


@bp.route('/maps/area/')
def area():
    args = request.args.get
    try:
        date_from = datetime.strptime(args('from'), '%Y-%m-%d')
    except (ValueError, TypeError):
        date_from = None
    try:
        date_to = datetime.strptime(args('to'), '%Y-%m-%d')
        date_to += timedelta(days=1)
    except (ValueError, TypeError):
        date_to = None

    points = MeasurePoint.query
    points = points.filter(MeasurePoint.longitude > args('west')
                  ).filter(MeasurePoint.longitude < args('east')
                  ).filter(MeasurePoint.latitude < args('north')
                  ).filter(MeasurePoint.latitude > args('south'))
    if date_from is not None:
        points = points.filter(MeasurePoint.timestamp >= date_from)
    if date_to is not None:
        points = points.filter(MeasurePoint.timestamp < date_to)

    measures = [_point_to_json_dict(p) for p in points]
    return jsonify(count=len(measures), points=measures)


CLUSTER_SENSOR_TYPES = ['Temperature', 'Humidity',
                        'OxidizingGas', 'ReducingGas']

@bp.route('/maps/cluster/', methods=['POST'])
def do_clustering():
    keys = request.get_json()

    points = []
    values = []
    types = set(CLUSTER_SENSOR_TYPES)
    for id, timestamp in keys:
        time = datetime.fromtimestamp(timestamp)
        point = MeasurePoint.query.get((id, time))
        value = {v.type_name: v.value for v in point.values.all()}
        if not set(value.keys()) >= types:
            continue
        # Normalization:
        value['OxidizingGas'] /= 1000
        value['ReducingGas'] /= 10000
        points.append(point)
        values.append(value)

    X = [[v[t] for t in CLUSTER_SENSOR_TYPES]
         for v in values]
    X = np.array(X)
    k = KMeans(n_clusters=2, init='k-means++')
    k.fit(X)
    score = silhouette_score(X, k.labels_)

    groups = [[_point_to_json_dict(p) for p, l in
              zip(points, k.labels_) if l == i] for i in
              range(max(k.labels_) + 1)]

    return jsonify(score=score, groups=groups)

