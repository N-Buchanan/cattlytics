from flask import render_template, flash, redirect, url_for, request
from app import app, db
from .forms import EditAnimalForm, AddWeightForm
from .models import Animal, Weight, Medicine
from .tables import AnimalTable, WeightTable
import datetime
from .algorithms.cow_math import calculate_weaning_weight


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    # table = AnimalTable(Animal.query.all())
    animals = Animal.query.all()
    for animal in animals:
        animal.weaned = animal.has_weaned()

    table = AnimalTable(animals)
    return render_template('index.html', title='Cattlytics', name='Test', table=table)


@app.route('/add', methods=['GET', 'POST'])
def add_animal():
    form = EditAnimalForm()
    if form.validate_on_submit():
        # animal = Animal(primary_tag=form.primary_tag.data,
        #                 birth_date=form.birth_date.data,
        #                 birth_weight=form.birth_weight.data)

        animal = Animal()
        # form.populate_obj(animal)
        animal.primary_tag = form.primary_tag.data
        animal.sex = form.sex.data
        animal.birth_date = form.birth_date.data
        animal.birth_weight = form.birth_weight.data
        animal.sex = animal.sex[:1].upper()

        # if the dam doesn't exist in the database, create it and get an id
        if form.dam.data:  # but only if a dam was given
            dam = Animal.query.filter_by(primary_tag=form.dam.data).first()
            if not dam:
                dam = Animal(primary_tag=form.dam.data)
                db.session.add(dam)
                db.session.commit()

            animal.dam = dam.id

        # same thing with the sire
        if form.sire.data:
            sire = Animal.query.filter_by(primary_tag=form.sire.data).first()
            if not sire:
                sire = Animal(primary_tag=form.sire.data)
                db.session.add(sire)
                db.session.commit()

            animal.sire = sire.id

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

    animal = db.session.query(Animal).filter_by(id=animal_id).first()
    form = EditAnimalForm()

    if form.validate_on_submit():
        animal = Animal.query.filter_by(id=form.id.data).first()

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
        if animal.dam:
            dam = Animal.query.filter_by(id=animal.dam).first()
            if dam:
                print(dam)
                form.dam.data = dam.primary_tag
        if animal.sire:
            sire = Animal.query.filter_by(id=animal.sire).first()
            if sire:
                form.sire.data = sire.primary_tag
        form.sex.data = animal.sex

    weights = Weight.query.filter_by(animal_id=animal.id)
    weights_table = WeightTable(weights)

    weight_form = AddWeightForm()
    weight_form.animal_id.data = animal.id

    animal_age = (datetime.date.today() - animal.birth_date).days

    adjusted_weight = None
    if animal.has_weaned():
        adjusted_weight = round(calculate_weaning_weight(animal))

    return render_template('edit.html', title='Cattlytics: Edit Animal', animal=animal.id,
                           form=form, weights_table=weights_table, weight_form=weight_form,
                           age=animal_age, adjusted_weight=adjusted_weight)


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
        weight.weaning = form.weaning.data

        db.session.add(weight)
        db.session.commit()

        print(form.animal_id.data)
        return redirect(url_for('edit_animal', animal_id=form.animal_id.data))

    return redirect(url_for('edit_animal', animal_id=form.animal_id.data))


@app.route('/delete_weight/<animal_id>/<date>', methods=['GET'])
def delete_weight(animal_id, date):
    weight = Weight.query.filter_by(animal_id=animal_id, date=date).first()

    db.session.delete(weight)
    db.session.commit()

    return redirect(url_for('edit_animal', animal_id=animal_id))


@app.route('/delete_animal/<animal_id>', methods=['GET'])
def delete_animal(animal_id):

    db.session.query(Animal).filter_by(id=animal_id).delete()
    db.session.query(Weight).filter_by(animal_id=animal_id).delete()
    db.session.query(Medicine).filter_by(animal_id=animal_id).delete()

    db.session.commit()

    return redirect(url_for('index'))
