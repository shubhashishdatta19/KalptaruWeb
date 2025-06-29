from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_ckeditor import CKEditor

db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()

# Create a single Flask-Admin instance
admin = Admin(name='Kalpataru Admin', template_mode='bootstrap3', url='/admin')

def create_app():
    import os
    from .models import SiteTheme
    
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    from .config import Config
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ckeditor.init_app(app)
    admin.init_app(app)  # Initialize the admin instance

    @app.context_processor
    def inject_theme():
        def get_theme():
            with app.app_context():
                return SiteTheme.get_active_theme()
        return dict(theme=get_theme())

    from . import models, forms, routes
    app.register_blueprint(routes.main)

    # Register admin views after admin is initialized
    from . import admin_views
    admin_views.register_admin_views()

    return app
