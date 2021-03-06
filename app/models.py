from app import db
from passlib.hash import sha512_crypt
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return '<User id:{} username:{} password:{} email:{}'\
            .format(self.id, self.username, self.password, self.email)

    def hash_password(self):
        self.password = sha512_crypt.hash(self.password)

    def verify_password(self, password):
        return sha512_crypt.verify(password, self.password)


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_tag = db.Column(db.String(15), index=True)
    birth_date = db.Column(db.Date)
    birth_weight = db.Column(db.Float)
    weights = db.relationship('Weight', backref='animal', lazy='dynamic')
    dam = db.Column(db.Integer, db.ForeignKey('animal.id'))
    sire = db.Column(db.Integer, db.ForeignKey('animal.id'))
    sex = db.Column(db.CHAR)
    owner = db.Column(db.Integer)

    def has_weaned(self):
        weight = Weight.query.filter_by(weaning=True, animal_id=self.id).first()
        return weight is not None


class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.String(15), db.ForeignKey('animal.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    weaning = db.Column(db.Boolean)



class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.Date)
    dose = db.Column(db.Float)
    unit = db.Column(db.String(10))
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))

