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
        self.user = None
        return False

