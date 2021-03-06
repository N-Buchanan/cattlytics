from flask_table import Table, Col, LinkCol, DateCol, BoolCol, OptCol
from .models import Animal

class AnimalTable(Table):

    classes = ['table']
    id = Col('ID')
    primary_tag = LinkCol('Primary Tag', attr='primary_tag', endpoint='edit_animal',
                          url_kwargs=dict(animal_id='id'))
    birth_date = DateCol('Birth Date')
    birth_weight = Col('Birth Weight')
    dam = OptCol('Dam')
    sire = OptCol('Sire')
    sex = Col('Sex')
    weaned = BoolCol('Weaned', yes_display='Weaned', no_display='')


class WeightTable(Table):
    classes = ['table']
    animal_id = Col('Animal ID')
    date = DateCol('Date')
    weight = Col('Weight')
    weaning = BoolCol('Weaning', yes_display='Weaning', no_display='')
    delete = LinkCol('Delete', endpoint='delete_weight', url_kwargs=dict(date='date', animal_id='animal_id'))


class MedicineTable(Table):
    classes = ['table']
    animal_id = Col('Animal ID')
    name = Col('Name')
    date = DateCol('Date')
    dose = Col('Dose')
    unit = Col('Unit')
    delete = LinkCol('Delete', endpoint='delete_medicine',
                     url_kwargs=dict(date='date', animal_id='animal_id', name='name'))

