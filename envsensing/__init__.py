from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__, instance_relative_config=True)

# Load configuration
app.config.from_object('config.default')
app.config.from_pyfile('config.py')

# Load extension
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Register views
from .views.home import home
app.register_blueprint(home)

# Register APIs
API_PREFIX = '/api'
from .resources import users
app.register_blueprint(users.bp, url_prefix=API_PREFIX)
