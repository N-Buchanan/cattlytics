from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, HiddenField, SelectField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class EditAnimalForm(FlaskForm):
    id = HiddenField()
    primary_tag = StringField('Primary Tag', validators=[DataRequired()])
    birth_date = DateField('Birth Date')
    birth_weight = FloatField('Birth Weight')
    submit = SubmitField('Save')
    dam = StringField('Dam')
    sire = StringField('Sire')
    sex = SelectField('Sex', choices=[('m', 'Male'), ('f', 'Female')])


class AddWeightForm(FlaskForm):
    weight = FloatField('Weight', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Save')
    animal_id = HiddenField()
    weaning = BooleanField()


class MedicineForm(FlaskForm):
    date = DateField('Date Administered')
    dose = FloatField('Dose Amount')
    unit = SelectField('Dose Unit', choices=[('ml', 'ml'), ('cc', 'cc')])
    animal_id = HiddenField()
