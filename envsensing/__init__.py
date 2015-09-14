from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask_restful import Api

app = Flask(__name__, instance_relative_config=True)

# Load configuration
app.config.from_object('config.default')
app.config.from_pyfile('config.py')

# Load extension
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
app.register_blueprint(api_bp, url_prefix='/api')

# Registe views
from .views.home import home
app.register_blueprint(home)

# API
from .resources.user import User
api.add_resource(User, '/user')

