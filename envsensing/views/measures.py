from flask import Blueprint, render_template, redirect, url_for, request, \
        flash
from flask.ext.login import login_required, login_user, logout_user, \
        current_user

from .. import db


bp = Blueprint("measures", __name__)


@bp.route('/')
@login_required
def index():
    return render_template('measures/index.html')


@bp.route('/tables/')
@login_required
def tables():
    devices = current_user.devices.all()
    return render_template('measures/tables.html', devices=devices)


@bp.route('/maps/')
@login_required
def maps():
    devices = current_user.devices.all()
    return render_template('measures/maps.html', devices=devices)
