from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__, instance_relative_config=True)

# Load configuration
app.config.from_object('config.default')
app.config.from_pyfile('config.py')

# Load extension
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
Bootstrap(app)

# Register views
from .views import home, users, measures
app.register_blueprint(home.bp)
app.register_blueprint(users.bp, url_prefix='/users')
app.register_blueprint(measures.bp, url_prefix='/measures')


# Register APIs
API_PREFIX = '/api'
from .resources import users, token, devices, measures
app.register_blueprint(users.bp, url_prefix=API_PREFIX + '/users')
app.register_blueprint(token.bp, url_prefix=API_PREFIX + '/token')
app.register_blueprint(devices.bp, url_prefix=API_PREFIX + '/devices')
app.register_blueprint(measures.bp,
        url_prefix=API_PREFIX + '/devices/<device_id>/measures')
