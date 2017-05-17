from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, HiddenField, SelectField, BooleanField, PasswordField
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


class AddMedicineForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = DateField('Date Administered', validators=[DataRequired()])
    dose = FloatField('Dose Amount', validators=[DataRequired()])
    unit = SelectField('Dose Unit', choices=[('ml', 'ml'), ('cc', 'cc')])
    submit = SubmitField('Save')
    animal_id = HiddenField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email Address')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    search_text = StringField("Search", validators=[DataRequired()])
    submit = SubmitField('Search')
