from wtforms.validators import ValidationError
import re

def phone_validator(form, field):
    pattern = r'^\+?[0-9]{10,12}$'
    if not re.match(pattern, field.data):
        raise ValidationError('Неверный формат номера телефона')

def password_complexity(form, field):
    if len(field.data) < 8:
        raise ValidationError('Пароль должен содержать минимум 8 символов')
    if not re.search(r'[A-Z]', field.data):
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
    if not re.search(r'[0-9]', field.data):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру')