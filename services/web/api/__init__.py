from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import os
import uuid

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("api.config.Config")
    db.init_app(app)
    #app.register_blueprint(test_page, url_prefix='/test')
    from api.route.image import image
    app.register_blueprint(image, url_prefix='/image')
    
    from api.route.gallery import gallery
    app.register_blueprint(gallery, url_prefix='/gallery')
    
    from api.route.user import user
    app.register_blueprint(user, url_prefix='/user')
    
    from api.route.likes import likes
    app.register_blueprint(likes, url_prefix='/likes')

    return app