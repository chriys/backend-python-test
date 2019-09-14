from wtforms import validators, Form, TextField, PasswordField, StringField

class LoginForm(Form):
    username = StringField('username', [validators.required()])
    password = PasswordField('password', [validators.required()])

class CreateTodoForm(Form):
    description = TextField('description', [validators.required(), validators.Length(min=4, max=255)])
