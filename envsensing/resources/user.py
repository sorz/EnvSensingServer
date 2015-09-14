from flask_restful import Resource, reqparse, abort

from .. import db
from ..models import User as UserModel

parser_user = reqparse.RequestParser()
parser_user.add_argument('username', required=True)
parser_user.add_argument('email', required=True)
parser_user.add_argument('password', required=True)


class User(Resource):
    def post(self):
        args = parser_user.parse_args()
        username, email = args['username'], args['email']

        if UserModel.query.filter_by(username=username).first() is not None:
            abort(400, message='Username exist.')
        if UserModel.query.filter_by(email=email).first() is not None:
            abort(400, message='Email exist.')

        user = UserModel(username, email)
        user.password = args['password']
        db.session.add(user)
        db.session.commit()
        return '', 204


