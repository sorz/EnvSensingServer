from functools import wraps
from flask import jsonify, request

from .. import app, csrf
from ..models.user import User


class APIException(Exception):
    # Reference:
    # http://flask.pocoo.org/docs/0.10/patterns/apierrors/
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = str(message)
        self.status_code = status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def csrf_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'with_basic_auth'):
            csrf.protect()
        return f(*args, **kwargs)
    return decorated_function


# Reference:
# https://github.com/mitsuhiko/flask/issues/686
class ParamJson(dict):
    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        else:
            raise APIException('Lack of argument: %s' % key)


def get_json_params():
    json = request.get_json()
    if json is None:
        raise APIException('JSON data is required.')
    return ParamJson(json)

