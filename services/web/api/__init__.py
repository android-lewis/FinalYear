from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string
from flask import Flask

import logging

db = SQLAlchemy()

def create_app(config_string='api.config.Config'):
    app = Flask(__name__)

    # App config loading
    cfg = import_string(str(config_string))()
    app.config.from_object(cfg)
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
    # Logging config
    logging.basicConfig(filename='api/logs/record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    
    # Initialise our DB
    db.init_app(app)

    # Register blueprint routes
    from api.route.image import image
    app.register_blueprint(image, url_prefix='/image')
    
    from api.route.gallery import gallery
    app.register_blueprint(gallery, url_prefix='/gallery')
    
    from api.route.user import user
    app.register_blueprint(user, url_prefix='/user')
    
    from api.route.likes import likes
    app.register_blueprint(likes, url_prefix='/likes')

    return app