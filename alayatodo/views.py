from alayatodo import app
from flask import (
    flash,
    redirect,
    render_template,
    request,
    session
    )
from flask_paginate import Pagination, get_page_args

from forms import CreateTodoForm
from alayatodo.models import object_as_dict, get_todos_count, Todo, User
from alayatodo.database import db_session


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')

    user = User.query.filter(User.username == username).first()
    if user and user.check_password(request.form.get('password')):
        session['user'] = object_as_dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todo.query.filter(Todo.id == id).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    todo = Todo.query.filter(Todo.id == id).first()
    return render_template('json.html', todo=todo)


@app.route('/todo/', methods=['GET'])
@app.route('/todo', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    todos = Todo.query.filter(Todo.user_id == session['user']['id']).offset(offset).limit(offset + per_page).all()

    pagination = Pagination(page=page, total=get_todos_count(session['user']['id']), record_name='todos', per_page=per_page,
                            css_framework='bootstrap', bs_version=3)

    return render_template('todos.html', todos=todos, page=page, pagination=pagination)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    form = CreateTodoForm(request.form)

    if form.validate():
        todo = Todo(session['user']['id'], form.description.data)
        db_session.add(todo)
        db_session.commit()
        flash('Todo successfully created!')

    # create a paginator to redirect the user to the last page after a todo has been added
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination = Pagination(page=page, total=get_todos_count(session['user']['id']), per_page=per_page)

    return redirect('/todo?page=%s' % pagination.total_pages)


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    db_session.delete(Todo.query.filter(Todo.id == id).first())
    db_session.commit()
    flash('Todo successfully deleted!')
    return redirect('/todo')

@app.route('/complete-todo/<id>', methods=['POST'])
def todo_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.filter(Todo.id == id).first()
    todo.completed = True
    db_session.add(todo)
    db_session.commit()
    flash('Todo successfully completed!')
    return redirect('/todo')
