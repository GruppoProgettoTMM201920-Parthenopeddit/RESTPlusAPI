from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pyfcm import FCMNotification

from config import config_by_name, Config, FCM_API_KEY

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
migrate = Migrate()
cors = CORS()
fcm = FCMNotification(FCM_API_KEY)


def create_app(config_name):
    app = Flask(__name__)
    configuration = config_by_name[config_name]
    app.config.from_object(configuration)

    db.init_app(app)
    flask_bcrypt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    return app
