from flask import render_template, flash, redirect, url_for, request, abort, session
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from .forms import EditAnimalForm, AddWeightForm, AddMedicineForm, LoginForm, UserRegistrationForm
from .models import Animal, Weight, Medicine, User
from .tables import AnimalTable, WeightTable, MedicineTable
import datetime
from .algorithms.cow_math import calculate_weaning_weight


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def authentication_failed(e):
    return render_template('404.html'), 401 # FIXME: need a 401 page


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


@app.route('/')
@app.route('/index')
@login_required
def index():
    # used to map internal database ids to human-readable primary_tag in the animal table
    name_dict = {}

    animals = Animal.query.filter_by(owner=current_user.id).all()
    for animal in animals:
        animal.weaned = animal.has_weaned()
        name_dict[animal.id] = animal.primary_tag

    table = AnimalTable(animals)
    table.dam.choices = name_dict
    table.sire.choices = name_dict
    return render_template('index.html', title='Cattlytics', name='Test', table=table)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return abort(401)
    # else:
    #     print('couldnt validate?')
    #     return abort(401)

    return render_template('login.html', login_form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_animal():
    form = EditAnimalForm()
    if form.validate_on_submit():
        # It's possible that we've already added this animal if the user previously added an animal and listed
        # Dam and Sire that did not yet exist. In that case we add them to the database anyway for ease of reference
        # so it's possible that this is that "shadow" animal we added. So we'll check the database first to see if any
        # such animal exists

        animal = Animal.query.filter_by(primary_tag=form.primary_tag.data, owner=current_user.id).first()

        # If there is an animal already with that primary_tag then we should check if we put it there or if the user did
        # The add animal form doesn't validate if they don't provide a birth weight so that's how we'll check who added it
        if animal is not None and animal.birth_weight is not None:
            # they added it so we should warn them that they are about to overwrite an existing animal
            return render_template('new_animal.html',
                                   title='Cattlytics: Add Animal',
                                   form=form,
                                   warning='There is already an animal with that primary tag. Please choose another one')

        if animal is None:
            animal = Animal()

        # at this point it's safe to add the animal to the database
        animal.primary_tag = form.primary_tag.data
        animal.sex = form.sex.data
        animal.birth_date = form.birth_date.data
        animal.birth_weight = form.birth_weight.data
        animal.sex = animal.sex[:1].upper() # only put 'M' or 'F' in database for simplicity with data analysis and querying

        # if the dam doesn't exist in the database, create it and get an id
        if form.dam.data:  # but only if a dam was given
            dam = Animal.query.filter_by(primary_tag=form.dam.data, owner=current_user.id).first()
            if not dam:
                dam = Animal(primary_tag=form.dam.data)
                db.session.add(dam)
                db.session.commit()

            animal.dam = dam.id

        # same thing with the sire
        if form.sire.data:
            sire = Animal.query.filter_by(primary_tag=form.sire.data, owner=current_user.id).first()
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
@login_required
def edit_animal(animal_id):

    animal = db.session.query(Animal).filter_by(id=animal_id).first()
    form = EditAnimalForm()

    if form.validate_on_submit():
        animal = Animal.query.filter_by(id=form.id.data, owner=current_user.id).first()

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
            dam = Animal.query.filter_by(id=animal.dam, owner=current_user.id).first()
            if dam:
                print(dam)
                form.dam.data = dam.primary_tag
        if animal.sire:
            sire = Animal.query.filter_by(id=animal.sire, owner=current_user.id).first()
            if sire:
                form.sire.data = sire.primary_tag
        form.sex.data = animal.sex

    weights = Weight.query.filter_by(animal_id=animal.id)
    weights_table = WeightTable(weights)

    weight_form = AddWeightForm()
    weight_form.animal_id.data = animal.id

    meds = Medicine.query.filter_by(animal_id=animal.id)
    medicine_table = MedicineTable(meds)

    medicine_form = AddMedicineForm()
    medicine_form.animal_id.data = animal_id

    animal_age = (datetime.date.today() - animal.birth_date).days

    adjusted_weight = None
    if animal.has_weaned():
        adjusted_weight = round(calculate_weaning_weight(animal))

    return render_template('edit.html', title='Cattlytics: Edit Animal', animal=animal.id,
                           form=form, weights_table=weights_table, weight_form=weight_form,
                           age=animal_age, adjusted_weight=adjusted_weight, medicine_table=medicine_table, medicine_form=medicine_form)


@app.route('/add_weight', methods=['POST'])
@login_required
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
@login_required
def delete_weight(animal_id, date):
    weight = Weight.query.filter_by(animal_id=animal_id, date=date).first()

    db.session.delete(weight)
    db.session.commit()

    return redirect(url_for('edit_animal', animal_id=animal_id))


@app.route('/delete_animal/<animal_id>', methods=['GET'])
@login_required
def delete_animal(animal_id):

    db.session.query(Animal).filter_by(id=animal_id).delete()
    db.session.query(Weight).filter_by(animal_id=animal_id).delete()
    db.session.query(Medicine).filter_by(animal_id=animal_id).delete()

    db.session.commit()

    return redirect(url_for('index'))

@app.route('/add_medicine', methods=['POST'])
@login_required
def add_medicine():
    form = AddMedicineForm()

    if form.validate():
        medicine = Medicine()
        form.populate_obj(medicine)
        db.session.add(medicine)
        db.session.commit()

    return redirect(url_for('edit_animal', animal_id=form.animal_id.data))


@app.route('/delete_medicine/<animal_id>/<date>/<name>', methods=['GET'])
def delete_medicine(animal_id, date, name):
    medicine = Medicine.query.filter_by(animal_id=animal_id, date=date, name=name).first()

    db.session.delete(medicine)
    db.session.commit()

    return redirect(url_for('edit_animal', animal_id=animal_id))


@app.route('/register', methods=['GET', 'POST'])
def add_user():
    form = UserRegistrationForm()

    if form.validate():
        user = User()
        form.populate_obj(user)

        # check that the user doesn't exist in the database already
        if User.query.filter_by(username=user.username).first() is None \
                and (not user.email or User.query.filter_by(email=user.email).first() is None):

            # they don't so we should add them
            user.hash_password()
            db.session.add(user)
            db.session.commit()

            # user created successfully so log them in and take them to the homepage
            login_user(user)
            # return redirect(request.args.get('next'))
            return redirect(url_for('index'))

            # TODO: user already exists in database, show an error

    return render_template('register_user.html', register_form=form)
