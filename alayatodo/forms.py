from wtforms import Form, TextField, validators

class CreateTodoForm(Form):
    description = TextField('description', [validators.Length(min=4, max=255)])