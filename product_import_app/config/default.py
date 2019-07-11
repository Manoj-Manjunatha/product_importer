"""Product import app default configuraion file."""

import os
from kombu import Exchange, Queue

SECRET_KEY = 'product_import_secret_key'

APP_ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

CSRF_ENABLED = True

DEBUG = True

STATIC_FOLDER = os.path.abspath(os.path.join(APP_ROOT_DIR, "static"))

MEDIA_FOLDER = os.path.join(STATIC_FOLDER, "media")

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ubatvpkgmjytel:2352dbe107ea8a612d44d79d19cd6b81d285a380bdb69e3d267f75465796a95d@ec2-23-23-199-181.compute-1.amazonaws.com:5432/d2h61297sds45m'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = True
CELERY_IMPORTS = ('product_import_app.tasks', )
CELERY_QUEUES = (
    Queue('import', Exchange('import'), routing_key='import'),
)
CELERY_ROUTES = {
    'tasks.product_import': {'queue': 'import', 'routing_key': 'import'},
}
