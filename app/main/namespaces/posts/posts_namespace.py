from flask import request
from flask_restplus import Namespace, Resource
from app.main.util.auth_decorator import token_authenticated
from app.main.namespaces.models_definition import get_post_model, get_new_post_model, get_content_with_comments_model, \
    ContentType
from app.main.namespaces.posts.post_services import save_new_post, get_post_by_id

api = Namespace('Posts', description="User's post framework")


@api.route("/")
class Posts(Resource):
    @token_authenticated
    @api.expect(get_new_post_model(api), validate=True)
    def post(self, token, user_id):
        """Publish new post"""
        payload = request.json
        return save_new_post(token, user_id, payload)


@api.route('/<int:post_id>')
@api.param('post_id', 'The Post identifier')
class GetPost(Resource):
    @token_authenticated
    @api.marshal_with(get_post_model(api))
    def get(self, token, user_id, post_id):
        """Get specific post"""
        return get_post_by_id(token, user_id, post_id)


@api.route('/<int:post_id>/comments')
@api.param('post_id', 'The Post identifier')
class GetPostWithComments(Resource):
    @token_authenticated
    @api.marshal_with(get_content_with_comments_model(api, ContentType.POST))
    def get(self, token, user_id, post_id):
        """Get specific post, with comments"""
        return get_post_by_id(token, user_id, post_id)
