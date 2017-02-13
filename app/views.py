from flask import render_template, flash, redirect, url_for, request
from app import app, db
from .forms import EditAnimalForm, AddWeightForm
from .models import Animal, Weight
from .tables import AnimalTable, WeightTable


@app.route('/')
@app.route('/index')
def index():
    table = AnimalTable(Animal.query.all())
    return render_template('index.html', title='Cattlytics', name='Test', table=table)


@app.route('/add', methods=['GET', 'POST'])
def add_animal():
    form = EditAnimalForm()
    if form.validate_on_submit():
        animal = Animal(primary_tag=form.primary_tag.data,
                        birth_date=form.birth_date.data,
                        birth_weight=form.birth_weight.data)

        db.session.add(animal)
        db.session.commit()

        # this needs to be after the database commit so that sqlalchemy can generate an id for animal
        # create first weight for animal with its birth date
        weight = Weight(animal_id=animal.id,
                       weight=animal.birth_weight,
                       date=animal.birth_date)

        db.session.add(weight)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('new_animal.html', title='Cattlytics: Add Animal',  form=form)


@app.route('/edit/<animal_id>', methods=['GET', 'POST'])
def edit_animal(animal_id):

    animal = db.session.query(Animal).filter_by(id=animal_id)[0]
    form = EditAnimalForm()

    if form.validate_on_submit():
        animal = Animal.query.filter_by(id=form.id.data)[0]

        print(animal_id)
        # animal.birth_date = form.birth_date.data
        # animal.birth_weight = form.birth_weight.data

        # animal = Animal()
        form.populate_obj(animal)
        db.session.add(animal)
        db.session.commit()
        return redirect(url_for('index'))

    if animal:
        form.primary_tag.data = animal.primary_tag
        form.birth_date.data = animal.birth_date
        form.birth_weight.data = animal.birth_weight
        form.id.data = animal.id

    weights = Weight.query.filter_by(animal_id=animal.id)
    weights_table = WeightTable(weights)

    weight_form = AddWeightForm()
    weight_form.animal_id.data = animal.id

    return render_template('edit.html', title='Cattlytics: Edit Animal', animal=animal.id,
                           form=form, weights_table=weights_table, weight_form=weight_form)


@app.route('/add_weight', methods=['POST'])
def add_weight():
    form = AddWeightForm()
    print(form.weight.data)

    # if form.validate():
    if form.weight.data and form.date.data:
        print('ns')
        weight = Weight()

        # populate from form data
        weight.date = form.date.data
        weight.weight = form.weight.data
        weight.animal_id = form.animal_id.data

        db.session.add(weight)
        db.session.commit()

        print(form.animal_id.data)
        return redirect(url_for('edit_animal', animal_id=form.animal_id.data))

    return redirect(url_for('edit_animal', animal_id=form.animal_id.data))
