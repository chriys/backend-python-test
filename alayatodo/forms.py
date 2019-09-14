from flask_wtf import FlaskForm
from wtforms import validators, TextField, PasswordField, StringField

class LoginForm(FlaskForm):
    username = StringField('username', [validators.required()])
    password = PasswordField('password', [validators.required()])

class CreateTodoForm(FlaskForm):
    description = TextField('description', [validators.required(), validators.Length(min=4, max=255)])
