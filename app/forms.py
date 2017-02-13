from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class EditAnimalForm(FlaskForm):
    primary_tag = StringField('Primary Tag', validators=[DataRequired()])
    birth_date = DateField('Birth Date')
    birth_weight = FloatField('Birth Weight')
    id = HiddenField()
    submit = SubmitField('Save')


class AddWeightForm(FlaskForm):
    weight = FloatField('Weight', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Save')
    animal_id = HiddenField()
