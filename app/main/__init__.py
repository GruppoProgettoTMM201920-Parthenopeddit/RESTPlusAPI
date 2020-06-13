from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
# TODO, NOITIFICATIONS
# from pyfcm import FCMNotification

from config import config_by_name # , TODO NOTIFICATIONS FCM_API_KEY

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
migrate = Migrate()
cors = CORS()
# TODO, NOITIFICATIONS
# fcm = FCMNotification(FCM_API_KEY)
whooshee = Whooshee()


def create_app(config_name):
    app = Flask(__name__)
    configuration = config_by_name[config_name]
    app.config.from_object(configuration)

    db.init_app(app)
    flask_bcrypt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    whooshee.init_app(app)

    return app
