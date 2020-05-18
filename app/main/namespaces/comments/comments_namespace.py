from flask import request
from flask_restplus import Namespace, Resource
from app.main.util.auth_decorator import token_authenticated
from app.main.namespaces.models_definition import get_new_comment_model, get_comment_model, ContentType, \
    get_content_with_comments_model
from app.main.namespaces.comments.comments_services import save_new_comment, get_comment_by_id

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
    @api.marshal_with(get_comment_model(api))
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
