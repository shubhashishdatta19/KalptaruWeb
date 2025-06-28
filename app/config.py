import os

class Config:
    SECRET_KEY = 'your_secret_key'  # Replace with a strong secret key
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
