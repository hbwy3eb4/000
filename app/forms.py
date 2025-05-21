from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class ProductForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Описание')
    stock = IntegerField('Количество на складе', validators=[NumberRange(min=0)])
    category = SelectField('Категория', coerce=int)
    image = FileField('Изображение')
    submit = SubmitField('Сохранить')

class CartAddForm(FlaskForm):
    quantity = IntegerField('Количество', validators=[
        DataRequired(),
        NumberRange(min=1, message='Количество должно быть больше 0')
    ])
    submit = SubmitField('Добавить в корзину')

class SearchForm(FlaskForm):
    query = StringField('Поиск', validators=[DataRequired()])
    category = SelectField('Категория', coerce=int, choices=[(0, 'Все категории')])
    submit = SubmitField('Найти')

class ContactForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')

class CheckoutForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    address = TextAreaField('Адрес доставки', validators=[DataRequired()])
    payment_method = SelectField('Способ оплаты', choices=[
        ('card', 'Банковская карта'),
        ('cash', 'Наличные при получении')
    ])
    submit = SubmitField('Оформить заказ')

