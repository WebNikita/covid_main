from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import USERS

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    status = SelectField(u'Статус заболевания', choices=[('Болел'), ('Не болел'), ('Болею')])
    contact = SelectField(u'Контакт с больным', choices=[('Контактировал'), ('Не контактировал'), ('Не знаю')])
    symptoms = StringField('Ваши симптомы', validators=[DataRequired()])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = USERS.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
