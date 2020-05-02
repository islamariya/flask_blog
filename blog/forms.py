from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, ValidationError

from models import User, Tags, PostsCategory


class LoginForm(FlaskForm):
    user_name = StringField("Имя пользователя: ", validators=[DataRequired()])
    password = PasswordField("Введите пароль: ",
                             validators=[InputRequired(), Length(min=8, max=100, message="Длина пароля 8 символов")])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Отправить")


class RegistrationForm(FlaskForm):
    user_name = StringField("Имя пользователя: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Введите пароль: ",
                             validators=[InputRequired(), Length(min=8, max=100, message="Длина пароля 8 символов"),
                                         EqualTo("confirm_password", message="Пароли не совпадают")])
    confirm_password = PasswordField("Повторно введите пароль: ", validators=[DataRequired()])
    submit = SubmitField("Отправить")

    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("Такой email уже зарегистрирован")
