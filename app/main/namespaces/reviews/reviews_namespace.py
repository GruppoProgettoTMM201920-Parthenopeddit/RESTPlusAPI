from flask import request
from flask_restplus import Namespace, Resource

from app.main.namespaces.models_definition import get_new_review_model, get_content_with_comments_model, \
    ContentType, get_content_model
from app.main.namespaces.reviews.reviews_services import save_new_review, get_review_by_id, dislike_review_by_id, \
    like_review_by_id
from app.main.util.auth_decorator import token_authenticated

api = Namespace('Reviews', description="User's reviews framework")


@api.route("/")
class Reviews(Resource):
    @token_authenticated
    @api.expect(get_new_review_model(api), validate=True)
    def post(self, token, user_id):
        """Publish new review"""
        payload = request.json
        return save_new_review(token, user_id, payload)


@api.route('/<int:review_id>')
@api.param('review_id', 'The Review identifier')
class GetReview(Resource):
    @token_authenticated
    @api.marshal_with(get_content_model(api, ContentType.REVIEW))
    def get(self, token, user_id, review_id):
        """Get specific post"""
        return get_review_by_id(token, user_id, review_id)


@api.route('/<int:review_id>/comments')
@api.param('review_id', 'The Review identifier')
class GetReviewWithComments(Resource):
    @token_authenticated
    @api.marshal_with(get_content_with_comments_model(api, ContentType.REVIEW))
    def get(self, token, user_id, review_id):
        """Get specific post, with comments"""
        return get_review_by_id(token, user_id, review_id)


@api.route('/<int:review_id>/like')
@api.param('review_id', 'The Review identifier')
class LikePost(Resource):
    @token_authenticated
    def post(self, token, user_id, review_id):
        """Express like to specific post"""
        return like_review_by_id(token, user_id, review_id)


@api.route('/<int:review_id>/dislike')
@api.param('review_id', 'The Review identifier')
class DislikePost(Resource):
    @token_authenticated
    def post(self, token, user_id, review_id):
        """Express dislike to specific post"""
        return dislike_review_by_id(token, user_id, review_id)
