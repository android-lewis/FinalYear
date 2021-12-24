from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import os
import uuid

from api.route.test import test_page

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    app.register_blueprint(test_page, url_prefix='/test')
    db.init_app(app)

    return app