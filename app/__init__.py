"""Product import app entry point."""
from flask import Flask
from flask_restful import Api
from flask_wtf.csrf import CsrfProtect

from celery import Celery

from api import configure_api
from models import db
from views import main

app = Flask(__name__)
app.config.from_object('config.default')

db.app = app
db.init_app(app)

csrf_protect = CsrfProtect(app)
app.register_blueprint(main)
api_manager = Api(app)
configure_api(api_manager)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
