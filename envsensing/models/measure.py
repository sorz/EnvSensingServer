from .. import db


class MeasurePoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    timestamp = db.Column(db.DateTime)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    accuracy = db.Column(db.Float)
    is_private = db.Column(db.Boolean, default=False)

    values = db.relationship('MeasureValue', backref='measure_point', lazy='dynamic')


    def __init__(self, device, timestamp, longitude, latitude, accuracy,
                 is_private=False):
        self.device_id = device.id
        self.timestamp = timestamp
        self.longitude = longitude
        self.latitude = latitude
        self.accuracy = accuracy


    def __repr__(self):
        return '<MeasurePoint %r>' % self.id


class MeasureValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measure_point_id = db.Column(db.Integer, db.ForeignKey('measure_point.id'))
    sensor_type = db.Column(db.Integer)
    value = db.Column(db.Float)


    def __init__(self, measure_point, sensor_type, value):
        self.measure_point_id = measure_point.id
        self.sensor_type = sensor_type
        self.value = value


    def __repr__(self):
        return '<MeasureValue %s: %.2f >' % (self.id, self.value)

