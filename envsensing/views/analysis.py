from flask import Blueprint, render_template, redirect, url_for, request, \
        flash
from flask.ext.login import login_required, login_user, logout_user, \
        current_user

from .. import db


bp = Blueprint("analysis", __name__)


@bp.route('/')
def index():
    return render_template('analysis/index.html')

