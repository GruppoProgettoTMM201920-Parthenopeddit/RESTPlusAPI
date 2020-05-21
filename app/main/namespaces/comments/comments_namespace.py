from flask import request
from flask_restplus import Namespace, Resource

from app.main.namespaces.comments.comments_services import save_new_comment, get_comment_by_id, dislike_comment_by_id, \
    like_comment_by_id
from app.main.namespaces.models_definition import get_new_comment_model, ContentType, get_content_with_comments_model, \
    get_content_model
from app.main.util.auth_decorator import login_required

api = Namespace('Comments', description="User's comments framework")

@api.route("/")
class Comments(Resource):
    @login_required
    @api.expect(get_new_comment_model(api), validate=True)
    @api.marshal_with(get_content_model(api, ContentType.COMMENT), code=201, description='Comment published successfully.')
    @api.response(201, 'Comment published successfully.')
    @api.response(300, 'Invalid payload. content_id needed.')
    @api.response(401, 'Commented post is private')
    @api.response(404, 'Cant find content to comment')
    def post(self, user):
        """Publish new comment to a user's content"""
        payload = request.json
        return save_new_comment(user, payload)


@api.route('/<int:comment_id>')
@api.param('comment_id', 'The Comment identifier')
class GetComment(Resource):
    @login_required
    @api.marshal_with(get_content_model(api, ContentType.COMMENT))
    @api.response(401, 'Commented post is private')
    @api.response(404, 'Cant find comment')
    @api.response(200, 'Comment successfully retrieved')
    def get(self, user, comment_id):
        """Get specific comment"""
        return get_comment_by_id(user, comment_id)


@api.route('/<int:comment_id>/comments')
@api.param('comment_id', 'The Comment identifier')
class GetCommentWithComments(Resource):
    @login_required
    @api.marshal_with(get_content_with_comments_model(api, ContentType.COMMENT))
    @api.response(401, 'Commented post is private')
    @api.response(404, 'Cant find comment')
    @api.response(200, 'Comment successfully retrieved')
    def get(self, user, comment_id):
        """Get specific comment, with comments"""
        return get_comment_by_id(user, comment_id)


@api.route('/<int:comment_id>/like')
@api.param('comment_id', 'The Comment identifier')
class LikePost(Resource):
    @login_required
    @api.response(401, 'Commented post is private')
    @api.response(404, 'Cant find comment')
    @api.response(210, 'liked comment')
    @api.response(211, 'removed like from comment')
    @api.response(212, 'removed dislike and liked comment')
    def post(self, user, comment_id):
        """Express like to specific post"""
        return like_comment_by_id(user, comment_id)


@api.route('/<int:comment_id>/dislike')
@api.param('comment_id', 'The Comment identifier')
class DislikePost(Resource):
    @login_required
    @api.response(401, 'Commented post is private')
    @api.response(404, 'Cant find comment')
    @api.response(210, 'disliked comment')
    @api.response(211, 'removed dislike from comment')
    @api.response(212, 'removed like and disliked comment')
    def post(self, user, comment_id):
        """Express dislike to specific post"""
        return dislike_comment_by_id(user, comment_id)
