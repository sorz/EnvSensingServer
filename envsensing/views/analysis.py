from flask import Blueprint, render_template, redirect, url_for, request, \
        flash
from flask.ext.login import login_required, login_user, logout_user, \
        current_user

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
