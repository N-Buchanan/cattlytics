from app import db


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_tag = db.Column(db.String(15), index=True, unique=True)
    birth_date = db.Column(db.Date)
    birth_weight = db.Column(db.Float)
    weights = db.relationship('Weight', backref='animal', lazy='dynamic')


class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.String(15), db.ForeignKey('animal.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)