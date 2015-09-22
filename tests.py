#!/usr/bin/env python3
import unittest
from flask.ext.testing import TestCase

from envsensing import app, db

# Reference:
# https://pythonhosted.org/Flask-Testing/

class MyTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'
        return app

    def setUp(self):
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserTest(MyTest):
    pass


if __name__ == '__main__':
    unittest.main()

