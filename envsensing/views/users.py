from flask import Blueprint, render_template, redirect, url_for, request
from flask.ext.login import login_required, login_user, logout_user

from ..models.user import User
from ..forms.users import LoginForm


bp = Blueprint("users", __name__)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)

        next = request.args.get('next')
        # TODO: validate the next
        return redirect(next or url_for('home.index'))

    return render_template('users/login.html', form=form)


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))

