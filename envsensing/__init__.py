from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


from .views.home import home

app.register_blueprint(home)

