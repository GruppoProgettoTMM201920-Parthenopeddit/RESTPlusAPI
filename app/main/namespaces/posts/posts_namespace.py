from flask import request
from flask_restplus import Namespace, Resource

from app.main.namespaces.models_definition import get_new_post_model, get_post_model, get_post_with_comments_model
from app.main.namespaces.posts.posts_services import save_new_post, get_post_by_id, dislike_post_by_id, like_post_by_id
from app.main.util.auth_decorator import login_required

api = Namespace('Posts', description="User's post framework")


@api.route("/")
class Posts(Resource):
    @login_required(api)
    @api.expect(get_new_post_model(api))
    @api.marshal_with(get_post_model(api), code=201, description='Post published successfully.')
    @api.response(201, 'Post published successfully.')
    @api.response(300, 'invalid board_id supplied')
    @api.response(401, 'Cant post to private group')
    @api.response(404, 'Cant find board')
    def post(self, user):
        """Publish new post"""
        return save_new_post(user, request)


@api.route('/<int:post_id>')
@api.param('post_id', 'The Post identifier')
class GetPost(Resource):
    @login_required(api)
    @api.marshal_with(get_post_model(api), code=200, description='Post successfully retrieved')
    @api.response(401, 'Post is private')
    @api.response(404, 'Cant find post')
    @api.response(200, 'Post successfully retrieved')
    def get(self, user, post_id):
        """Get specific post"""
        return get_post_by_id(user, post_id)


@api.route('/<int:post_id>/comments')
@api.param('post_id', 'The Post identifier')
class GetPostWithComments(Resource):
    @login_required(api)
    @api.marshal_with(get_post_with_comments_model(api), code=200, description='Post successfully retrieved')
    @api.response(401, 'Post is private')
    @api.response(404, 'Cant find post')
    @api.response(200, 'Post successfully retrieved')
    def get(self, user, post_id):
        """Get specific post, with comments"""
        return get_post_by_id(user, post_id)


@api.route('/<int:post_id>/like')
@api.param('post_id', 'The Post identifier')
class LikePost(Resource):
    @login_required(api)
    @api.response(401, 'Post is private')
    @api.response(404, 'Cant find post')
    @api.response(210, 'liked post')
    @api.response(211, 'removed like from post')
    @api.response(212, 'removed dislike and liked post')
    def post(self, user, post_id):
        """Express like to specific post"""
        return like_post_by_id(user, post_id)


@api.route('/<int:post_id>/dislike')
@api.param('post_id', 'The Post identifier')
class DislikePost(Resource):
    @login_required(api)
    @api.response(401, 'Post is private')
    @api.response(404, 'Cant find post')
    @api.response(210, 'liked post')
    @api.response(211, 'removed like from post')
    @api.response(212, 'removed dislike and liked post')
    def post(self, user, post_id):
        """Express dislike to specific post"""
        return dislike_post_by_id(user, post_id)
