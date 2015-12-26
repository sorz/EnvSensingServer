from .. import db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    device_id = db.Column(db.String(16))
    name = db.Column(db.String(30))

    measure_points = db.relationship('MeasurePoint', backref='device', lazy='dynamic')


    def __init__(self, user, device_id, name):
        self.user_id = user.id
        self.device_id = device_id
        self.name = name


    def __repr__(self):
        return '<Device %r>' % self.name

