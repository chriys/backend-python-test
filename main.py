"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app
from alayatodo.models import User
from alayatodo.database import db_session


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, ex:
        print ex.output
        os.exit(1)

def encrypt_passwords():
    users = User.query.all()
    for user in users:
        user.set_password(user.password)
    db_session.add_all(users)
    db_session.commit()


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        encrypt_passwords()
        print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True)
