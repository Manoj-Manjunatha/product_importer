"""Product import app entry point."""
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Command
from flask_wtf.csrf import CsrfProtect

from views import main
from models import db

app = Flask(__name__)
app.config.from_object('config.default')

db.app = app
db.init_app(app)

csrf_protect = CsrfProtect(app)
app.register_blueprint(main)
api_manager = Api(app)


class DevServer(Command):
    """Runs the Flask development server."""

    def __call__(self, app, **kwargs):
        """Call app run method."""
        self.app = app
        self.app.run()


manager = Manager(app)
Migrate(app, db)

manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db
}))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
