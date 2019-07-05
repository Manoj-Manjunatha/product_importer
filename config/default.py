"""Product import app default configuraion file."""

import os

SECRET_KEY = 'product_import_secret_key'

APP_ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

CSRF_ENABLED = True

DEBUG = True

STATIC_FOLDER = os.path.abspath(os.path.join(APP_ROOT_DIR, "static"))

MEDIA_FOLDER = os.path.join(STATIC_FOLDER, "media")

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://product_user:product_user@127.0.0.1:5432/product_importer'
SQLALCHEMY_TRACK_MODIFICATIONS = False
