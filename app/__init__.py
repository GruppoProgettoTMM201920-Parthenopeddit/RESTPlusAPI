from flask import Blueprint
from flask_restplus import Api
from .main.namespaces.auth_namespace import api as auth_namespace
from .main.namespaces.post_namespace import api as post_namespace
from .main.namespaces.comments_namespace import api as comments_namespace

blueprint = Blueprint('api', __name__)
authorizations = {
    'BasicLogin': {
        'type': 'basic',
        'in': 'header',
        'name': 'authorization'
    }
}
api = Api(
    blueprint,
    title='Parthenopeddit Project API',
    version='1.0',
    description='University of Naples "Parthenope" social media API for students',
    authorizations=authorizations,
    security='BasicLogin'
)

api.add_namespace(auth_namespace, path='/auth')
api.add_namespace(post_namespace, path='/post')
api.add_namespace(comments_namespace, path='/comments')
