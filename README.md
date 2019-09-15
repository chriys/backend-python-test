Alayacare Python skill test
===========================


### Requirements
* python 2.7
* virtualenv
* sqlite3

### Installation
```sh
virtualenv .
bin/pip install -r requirements.txt
bin/python main.py initdb
bin/python main.py
```

### Application
The TODO App allows a user to add reminders of thing he needs to do. Here are the requirement for the app.
* Users can add, delete and see their todos.
* All the todos are private, users can't see other user's todos.
* Users must be logged in order to add/delete/see their todos.

Credentials:
* username: **user1**
* password: **user1**

#### Homepage:
![Homepage](/web/img/homepage.png?raw=true "Homepage")

#### Login page:
![Login page](/web/img/login-page.png?raw=true "Login page")

#### Todos:
![Todos](/web/img/todos.png?raw=true "Todos")

### Documentation
This app use [Flask](http://flask.pocoo.org/docs/0.10/).
