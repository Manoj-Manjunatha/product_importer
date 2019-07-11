from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Command


from app import app
from app.models import db


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
