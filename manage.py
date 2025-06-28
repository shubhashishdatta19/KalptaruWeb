from app import app, db
from flask_migrate import Migrate
from flask_script import Manager, Command

# Define a custom command to wrap Flask-Migrate commands
class DBCommand(Command):
    def run(self, *args, **kwargs):
        # This is a simplified wrapper. In a real scenario, you'd parse args
        # and call the appropriate Flask-Migrate function.
        # For 'init', 'migrate', 'upgrade', 'downgrade', etc.
        # For now, we'll just instruct the user to use 'flask db' directly.
        print("Please use 'flask db <command>' instead of 'python manage.py db <command>'.")
        print("Example: 'flask db init', 'flask db migrate', 'flask db upgrade'")

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', DBCommand())

if __name__ == '__main__':
    manager.run()
