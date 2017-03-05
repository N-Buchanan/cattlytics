from app.models import Animal, Weight
from app import db
import datetime

BIF_STANDARD_ADJUSTMENT_FACTORS = {
    2: {'birth_weight': 8,
        'male': 60,
        'female': 54},
    3: {'birth_weight': 5,
        'male': 40,
        'female': 36},
    4: {'birth_weight': 2,
        'male': 20,
        'female': 18},
    5: {'birth_weight': 0,
        'male': 0,
        'female': 0},
    11: {'birth_weight': 3,
         'male': 20,
         'female': 18}
}


def get_adjustment_factor(age_of_dam_at_birth_of_calf):
    if age_of_dam_at_birth_of_calf < 5:
        age = age_of_dam_at_birth_of_calf
    elif 5 <= age_of_dam_at_birth_of_calf <= 10:
        age = 5
    else:
        age = 11

    return BIF_STANDARD_ADJUSTMENT_FACTORS[age]


def calculate_weaning_weight(cow):
    weaning = Weight.query.filter_by(weaning=True, animal_id=cow.id).first()

    weaning_age = (weaning.date - cow.birth_date).days
    return ((weaning.weight - cow.birth_weight) / weaning_age) * 205
