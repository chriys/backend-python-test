from flask_wtf import FlaskForm
from wtforms import validators, TextField, PasswordField, StringField
from models import User
import safe

class LoginForm(FlaskForm):
    username = StringField('username', [validators.required()])
    password = PasswordField('password', [validators.required()])

class RegistrationForm(FlaskForm):
    username = StringField('username', [validators.required(), validators.Length(min=4)])
    password = PasswordField('password', [validators.required()])
    password2 = PasswordField('repeat password', [validators.required(), validators.EqualTo('password')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise validators.ValidationError('Please use a different username.')

    def validate_password(self, password):
        if not bool(safe.check(password.data, length=4, level=2)):
            raise validators.ValidationError('Password too predictable. Try adding a capital letters, numbers or special characters.')

class CreateTodoForm(FlaskForm):
    description = TextField('description', [validators.required(), validators.Length(min=4, max=255)])
