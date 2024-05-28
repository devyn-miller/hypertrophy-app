from wtforms import ValidationError

def validate_positive_number(form, field):
    if field.data <= 0:
        raise ValidationError('Field must be positive.')

def validate_user_age(form, field):
    if field.data < 18:
        raise ValidationError('You must be at least 18 years old to register.')

