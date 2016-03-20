from flask import Blueprint, render_template, redirect, url_for, request, \
        flash, jsonify
from flask.ext.login import login_required, login_user, logout_user, \
        current_user
from datetime import datetime, timedelta

from .. import db
from ..models.user import User
from ..models.device import Device
from ..models.measure import MeasurePoint


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
    print(points)

    measures = []
    for p in points:
        item = dict(timestamp=p.timestamp.timestamp(),
                    latitude=p.latitude, longitude=p.longitude,
                    accuracy=p.accuracy, values=[])
        for value in p.values.all():
            item['values'].append(dict(type=value.type_name, value=value.value))
        measures.append(item)
    return jsonify(count=len(measures), points=measures)

