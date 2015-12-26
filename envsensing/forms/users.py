from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SubmitField, validators

from ..models.user import User

class LoginForm(Form):
    username = TextField('Username', [validators.Length(max=30)])
    password = PasswordField('Password', [validators.Required()])
    submit = SubmitField('Log in')

    def validate(self):
        if super().validate():
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                if user.verify_password(self.password.data):
                    self.user = user
                    return True
            error = 'Username and/or password not matched.'
            self.username.errors.append(error)
            self.password.errors.append(error)
        self.user = None
        return False


class ChangePasswordForm(Form):
    old_password = PasswordField('Current password', [validators.Required()])
    new_password = PasswordField('New password', [validators.Length(min=6)])
    new_password_2 = PasswordField('New password again',
                                   [validators.Length(min=6)])
    submit = SubmitField('Change')

    def validate(self):
        if not super().validate():
            return False
        if self.new_password.data != self.new_password_2.data:
            self.new_password.errors.append('Two new passwords mismatch.')
            return False
        return True

