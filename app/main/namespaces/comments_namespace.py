from flask import request
from flask_restplus import Namespace, Resource
from app.main.auth.decorators import token_authenticated
from app.main.model.models_definition import get_new_comment_model, get_comment_model, ContentType, \
    get_content_with_comments_model
from app.main.services.comments_services import save_new_comment, get_post_comments, get_comment_comments, get_comment

api = Namespace('Comments', description="User's comments framework")


@api.route('/<comment_id>')
@api.param('comment_id', 'The Comment identifier')
class GetPost(Resource):

    @token_authenticated
    @api.marshal_list_with(get_comment_model(api))
    def get(self, token, user_id, comment_id):
        """Get comment"""
        return get_comment(token, user_id, comment_id)


@api.route('/<comment_id>/comments')
@api.param('comment_id', 'The Comment identifier')
class GetPost(Resource):
    @token_authenticated
    @api.marshal_list_with(get_content_with_comments_model(api, ContentType.COMMENT))
    def get(self, token, user_id, comment_id):
        """Get comments with comments"""
        return get_post_comments(token, user_id, comment_id)


@api.route('/to_post/<post_id>')
@api.param('post_id', 'The Post identifier')
class NewCommentToPost(Resource):

    @token_authenticated
    @api.expect(get_new_comment_model(api), validate=True)
    def post(self, token, user_id, post_id):
        """Publish new comment to a Post"""
        payload = request.json
        return save_new_comment(token, user_id, payload, post_id, "post")

    @token_authenticated
    @api.marshal_list_with(get_content_with_comments_model(api, ContentType.COMMENT))
    def get(self, token, user_id, post_id):
        """Get comments to a Post"""
        return get_post_comments(token, user_id, post_id)


@api.route('/to_comment/<comment_id>')
@api.param('comment_id', 'The Comment identifier')
class NewCommentToComment(Resource):

    @token_authenticated
    @api.expect(get_new_comment_model(api), validate=True)
    def post(self, token, user_id, comment_id):
        """Publish new comment to a Comment"""
        payload = request.json
        return save_new_comment(token, user_id, payload, comment_id, "comment")

    @token_authenticated
    @api.marshal_list_with(get_content_with_comments_model(api, ContentType.COMMENT))
    def get(self, token, user_id, comment_id):
        """Get comments to a comment"""
        return get_comment_comments(token, user_id, comment_id)
