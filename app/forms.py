from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import EqualTo, InputRequired, Email

from app import db
from app.custom_vallidators import Unique, Exists
from app.models import User, Event


class CreateUserForm(FlaskForm):
    username = StringField("Ваш логин:", validators=[InputRequired(), Unique(User, User.username, message='Такой пользователь уже существует!')])
    password = PasswordField("Пароль:", [InputRequired(), EqualTo('confirm', message='Пароли должны совпадать!')])
    confirm = PasswordField("Повторие пароль:", validators=[InputRequired(), EqualTo('password', message='Пароли должны совпадать!')])
    submit_button = SubmitField('Кнопочка')


class LoginForm(FlaskForm):
    username = StringField("Ваш логин:", validators=[InputRequired(), Exists(User, User.username, message='Пользователя с таким логином я не нашел... Вы похоже что-то напутали.')])
    password = PasswordField("Пароль:", validators=[InputRequired()])
    submit_button = SubmitField('Кнопочка')


class LogoutForm(FlaskForm):
    logout_or_not = BooleanField('Вы точно хотите выйти?')
    submit_button = SubmitField('Кнопочка')


class EventForm(FlaskForm):
    datetime_end = DateTimeField('Дата и время окончания:', id='datepick', validators=[InputRequired()])
    topic = StringField('Тема:', validators=[InputRequired()])
    description = StringField('Описание:', validators=[InputRequired()])
    submit_button = SubmitField('Кнопочка')


class EventDeleteForm(FlaskForm):
    delete_or_not = BooleanField('Вы точно хотите удалить это событие?')
    submit_button = SubmitField('Кнопочка')



