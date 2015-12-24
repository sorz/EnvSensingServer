from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user

from ..models.user import User


bp = Blueprint("users", __name__)


@bp.route('/login')
def login():
    return render_template('users/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))

