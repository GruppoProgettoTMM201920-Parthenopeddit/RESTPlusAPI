import os

basedir = os.path.abspath(os.path.dirname(__file__))
COMMENTS_RECURSIVE_DEPTH = 5
DEFAULT_POSTS_PER_PAGE_AMOUNT = 20
BYPASS_LOGIN = True

# Your api-key can be gotten from:
# https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
FCM_API_KEY = os.getenv('FCM_API_KEY', 'AAAAWnKOp40:APA91bGJX8NxPqQAu5Hlw5lzM4VF7pVnYW8OMRNuvn2XoKz2IltZ4JbuyYsmf5Mt3vMBxV5KqjECpRpLDpHhWaba31NvXo7CfH4JllSl-TbTdI_9OgSooaGuU6vRjD-o2eoqeT24vaHi')

# Not required proxy dict
FCM_PROXY_DICT = {
    "http": "http://127.0.0.1",
    "https": "http://127.0.0.1",
}


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db'))
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db'))


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
