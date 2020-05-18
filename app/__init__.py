from flask import Blueprint
from flask_restplus import Api

from app.main.namespaces.auth.auth_namespace import api as auth_namespace
from app.main.namespaces.comments.comments_namespace import api as comments_namespace
from app.main.namespaces.posts.posts_namespace import api as post_namespace
from app.main.namespaces.reviews.reviews_namespace import api as reviews_namespace

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
api.add_namespace(post_namespace, path='/posts')
api.add_namespace(comments_namespace, path='/comments')
api.add_namespace(reviews_namespace, path='/reviews')
