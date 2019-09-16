from alayatodo import app
from flask import flash, redirect, render_template, request, session, abort, url_for, jsonify
from flask_paginate import Pagination, get_page_args
from forms import CreateTodoForm, LoginForm, RegistrationForm
from alayatodo.models import object_as_dict, get_todos_count, Todo, User
from alayatodo.database import db_session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todos'))
    # get the user
    user = User.query.filter_by(username=request.form.get('username')).first()

    form = LoginForm(request.form)
    if form.validate_on_submit():
        # move to user.authenticate
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next = request.args.get('next')
            if not is_safe_url(next):
                next = url_for('todos')
            return redirect(next or url_for('todos'))
        else:
            flash("Invalid Username or Password", 'danger')

    return render_template('login.html', form=form)


def is_safe_url(url):
    return url and url_parse(url).netloc != ''


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(form.username.data)
        user.set_password(form.password.data)
        db_session.add(user)
        db_session.commit()
        flash('Congratulations, you are now registered with the username: %s' % form.username.data, 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/todo/<id>', methods=['GET'])
@login_required
def todo(id):
    todo = Todo.query.filter(Todo.id == id).first()
    if not todo or not todo.belongs_to(current_user.id):
        flash("Oups... Doesn't look like the todo you're looking for exists.", 'danger')
        return redirect('/todo')
    return render_template('todo.html', todo=todo)


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    todo = Todo.query.filter(Todo.id == id).first()
    if not todo or not todo.belongs_to(current_user.id):
        flash("Oups... Doesn't look like the todo you're looking for exists.", 'danger')
        return redirect('/todo')
    return render_template('json.html', todo=todo)


@app.route('/todo/', methods=['GET'])
@app.route('/todo', methods=['GET'])
@login_required
def todos():
    # create a paginator to redirect the user to the last page after a todo has been added
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    todos = Todo.query.filter(Todo.user_id == current_user.get_id()).offset(offset).limit(offset + per_page).all()

    pagination = Pagination(page=page, total=get_todos_count(current_user.get_id()), record_name='todos', per_page=per_page,
                            css_framework='bootstrap', bs_version=3)
    return render_template('todos.html', todos=todos, page=page, pagination=pagination)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    # create a paginator to redirect the user to the last page after a todo has been added
    page, per_page, offset = get_page_args(page_parameter='page',
                                        per_page_parameter='per_page')
    todos = Todo.query.filter(Todo.user_id == current_user.get_id()).offset(offset).limit(offset + per_page).all()
    pagination = Pagination(page=page, total=get_todos_count(current_user.get_id()), per_page=per_page)

    form = CreateTodoForm(request.form)

    if form.validate_on_submit():
        todo = Todo(current_user.get_id(), form.description.data)
        db_session.add(todo)
        db_session.commit()
        flash('Todo successfully created!', 'success')
        return redirect('/todo?page=%s' % pagination.total_pages)

    return render_template('todos.html', form=form, todos=todos, page=page, pagination=pagination)


@app.route('/todo/<id>', methods=['POST'])
@login_required
def todo_delete(id):
    todo = Todo.query.filter(Todo.id == id).first()
    if not todo or not todo.belongs_to(current_user.id):
        flash("Oups... Doesn't look like the todo you're looking for exists.", 'danger')
        return redirect('/todo')
    db_session.delete(todo)
    db_session.commit()
    flash('Todo successfully deleted!', 'success')
    return redirect('/todo')

@app.route('/complete-todo/<id>', methods=['POST'])
@login_required
def todo_complete(id):
    todo = Todo.query.filter(Todo.id == id).first()
    if not todo or not todo.belongs_to(current_user.id):
        flash_message = "Oups... Doesn't look like the todo you're looking for exists."
        return jsonify(id=id, completed=False, flash=flash_message)

    todo.toggle_completion()
    flash_message= 'Todo successfully completed!' if todo.completed else ''
    db_session.add(todo)
    db_session.commit()
    return jsonify(
        id=todo.id,
        completed=todo.completed,
        completed_at=todo.completed_at,
        flash=flash_message
    )
