import os

from flask import render_template

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server

from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(use_debugger=True))

if __name__ == '__main__':
    manager.run()
