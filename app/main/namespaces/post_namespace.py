from flask import request
from flask_restplus import Namespace, Resource
from app.main.auth.decorators import token_authenticated
from app.main.model.models_definition import get_post_model, get_new_post_model, get_post_with_comments_model
from app.main.services.post_services import save_new_post, get_post_by_id, get_all_posts

api = Namespace('Posts', description="User's post framework")


@api.route('/new')
class NewPost(Resource):
    @token_authenticated
    @api.expect(get_new_post_model(api), validate=True)
    def post(self, token, user_id):
        """Publish new post"""
        payload = request.json
        return save_new_post(token, user_id, payload)


@api.route('/<post_id>')
@api.param('post_id', 'The Post identifier')
class GetPost(Resource):
    @token_authenticated
    @api.marshal_with(get_post_model(api))
    def get(self, token, user_id, post_id):
        """Get specific post"""
        return get_post_by_id(token, user_id, post_id)


@api.route('/<post_id>/comments')
@api.param('post_id', 'The Post identifier')
class GetPost(Resource):
    @token_authenticated
    @api.marshal_with(get_post_with_comments_model(api))
    def get(self, token, user_id, post_id):
        """Get specific post"""
        return get_post_by_id(token, user_id, post_id)


@api.route('/all')
class GetAllPosts(Resource):
    @token_authenticated
    @api.marshal_list_with(get_post_model(api))
    def get(self, token, user_id):
        """Get all posts"""
        return get_all_posts(token, user_id)
