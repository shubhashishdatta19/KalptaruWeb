from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_ckeditor import CKEditor

db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='Kalpataru Admin', template_mode='bootstrap3')
ckeditor = CKEditor()

def create_app():
    import os
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    from .config import Config
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    ckeditor.init_app(app)

    from . import models, forms, routes
    import app.admin as admin_module
    admin_module.register_admin_views(app)

    return app
