from flask import request
from flask_restplus import Namespace, Resource

from app.main.namespaces.comments.comments_services import save_new_comment, get_comment_by_id, dislike_comment_by_id, \
    like_comment_by_id
from app.main.namespaces.models_definition import get_new_comment_model, ContentType, get_content_with_comments_model, \
    get_content_model
from app.main.util.auth_decorator import token_authenticated

api = Namespace('Comments', description="User's comments framework")

@api.route("/")
class Comments(Resource):
    @token_authenticated
    @api.expect(get_new_comment_model(api), validate=True)
    def post(self, token, user_id):
        """Publish new comment to a user's content"""
        payload = request.json
        return save_new_comment(token, user_id, payload)


@api.route('/<int:comment_id>')
@api.param('comment_id', 'The Comment identifier')
class GetComment(Resource):
    @token_authenticated
    @api.marshal_with(get_content_model(api, ContentType.COMMENT))
    def get(self, token, user_id, comment_id):
        """Get specific comment"""
        return get_comment_by_id(token, user_id, comment_id)


@api.route('/<int:comment_id>/comments')
@api.param('comment_id', 'The Comment identifier')
class GetCommentWithComments(Resource):
    @token_authenticated
    @api.marshal_with(get_content_with_comments_model(api, ContentType.COMMENT))
    def get(self, token, user_id, comment_id):
        """Get specific comment, with comments"""
        return get_comment_by_id(token, user_id, comment_id)


@api.route('/<int:comment_id>/like')
@api.param('comment_id', 'The Comment identifier')
class LikePost(Resource):
    @token_authenticated
    def post(self, token, user_id, comment_id):
        """Express like to specific post"""
        return like_comment_by_id(token, user_id, comment_id)


@api.route('/<int:comment_id>/dislike')
@api.param('comment_id', 'The Comment identifier')
class DislikePost(Resource):
    @token_authenticated
    def post(self, token, user_id, comment_id):
        """Express dislike to specific post"""
        return dislike_comment_by_id(token, user_id, comment_id)
