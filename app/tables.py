from flask_table import Table, Col, LinkCol, DateCol


class AnimalTable(Table):
    classes = ['table']
    id = Col('ID')
    primary_tag = LinkCol('Primary Tag', attr='primary_tag', endpoint='edit_animal',
                          url_kwargs=dict(animal_id='id'))
    birth_date = DateCol('Birth Date')
    birth_weight = Col('Birth Weight')


class WeightTable(Table):
    classes = ['table']
    date = DateCol('Date')
    weight = Col('Weight')