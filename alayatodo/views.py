from alayatodo import app
from flask import (
    g,
    flash,
    redirect,
    render_template,
    request,
    session
    )
from flask_paginate import Pagination, get_page_args

from forms import CreateTodoForm
from alayatodo.models import Todo


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
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
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

    todos_count = g.db.execute("SELECT COUNT(*) as total FROM todos").fetchone()

    cur = g.db.execute("SELECT * FROM todos LIMIT %s, %s" % (offset, offset + per_page))
    todos = cur.fetchall()

    pagination = Pagination(page=page, total=todos_count[0], record_name='todos', per_page=per_page,
                            css_framework='bootstrap', bs_version=3)

    return render_template('todos.html', todos=todos, page=page, pagination=pagination, last=pagination.total_pages)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    form = CreateTodoForm(request.form)

    if form.validate():
        g.db.execute(
            "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
            % (session['user']['id'], form.description.data)
        )
        g.db.commit()
        flash('Todo successfully created!')

    # create a paginator to redirect the user to the last page after a todo has been added
    todos_count = g.db.execute("SELECT COUNT(*) as total FROM todos").fetchone()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination = Pagination(page=page, total=todos_count[0], per_page=per_page)

    return redirect('/todo?page=%s' % pagination.total_pages)


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    flash('Todo successfully deleted!')
    return redirect('/todo')
