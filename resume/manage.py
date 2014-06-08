from flask.ext.script import Manager

from sched.app import app, db, user_datastore
from sched.models import Role

# By default, Flask-Script adds the 'runserver' and 'shell' commands to
# interact with the Flask application. Add additional commands using the
# `@manager.command` decorator, where Flask-Script will create help
# documentation using the function's docstring. Try it, and call `python
# manage.py -h` to see the outcome.
manager = Manager(app)


@manager.command
def create_tables():
    "Create relational database tables."
    db.create_all()
    db.session.add(Role(name='ROLE_ADMIN', description='admin'))
    db.session.add(Role(name='ROLE_USER', description='user'))
    db.session.add(Role(name='ROLE_COMPANY_SILVER', description='company silver'))
    db.session.add(Role(name='ROLE_COMPANY_FREE', description='company free'))
    db.session.add(Role(name='ROLE_COMPANY_PREMIUM', description='company premium'))
    db.session.add(Role(name='ROLE_COMPANY_PREMIUM_PRO', description='company premium pro'))
    db.session.add(Role(name='ROLE_SCHOOL', description='school'))
    db.session.add(Role(name='ROLE_CANDIDATE', description='candidate'))
    db.session.commit()


@manager.command
def drop_tables():
    "Drop all project relational database tables. THIS DELETES DATA."
    db.drop_all()

@manager.option('-i', '--id', help='User id or email')
def add_admin(id):
    user = user_datastore.get_user(id)
    role = user_datastore.find_role('ROLE_ADMIN')
    user_datastore.add_role_to_user(user, role)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
