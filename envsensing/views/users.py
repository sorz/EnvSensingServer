from flask import Blueprint, render_template, redirect, url_for, request, \
        flash
from flask.ext.login import login_required, login_user, logout_user, \
        current_user

from .. import db
from ..models.user import User
from ..forms.users import LoginForm, ChangePasswordForm


bp = Blueprint("users", __name__)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)

        next = request.args.get('next')
        # TODO: validate the next
        flash('Welcome, %s.' % form.user.username, 'success')
        return redirect(next or url_for('users.me'))

    return render_template('users/login.html', form=form)


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have logged out.', 'success')
    return redirect(url_for('home.index'))


@bp.route('/me/')
@login_required
def me():
    return render_template('users/me.html')


@bp.route('/me/password/', methods=['GET', 'POST'])
@login_required
def password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('users.me'))
        else:
            form.old_password.errors.append('Current password incorrect.')

    return render_template('users/password.html', form=form)

