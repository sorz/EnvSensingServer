from .. import app, db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(30))


    def __init__(self, user, name):
        self.user_id = user.id
        self.name = name


    def __repr__(self):
        return '<Device %r>' % self.name

