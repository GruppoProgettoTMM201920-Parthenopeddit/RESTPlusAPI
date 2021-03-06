from flask import request
from flask_restplus import Namespace, Resource

from app.main.namespaces.models_definition import get_new_review_model, get_review_model, \
    get_review_with_comments_model, get_like_dislike_score_model
from app.main.namespaces.reviews.reviews_services import save_new_review, get_review_by_id, dislike_review_by_id, \
    like_review_by_id
from app.main.namespaces.auth.auth_decorator import login_required

api = Namespace('Reviews', description="User's reviews framework")


@api.route("/")
class Reviews(Resource):
    @login_required(api)
    @api.expect(get_new_review_model(api))
    @api.marshal_with(get_review_model(api), code=201, description='Review published successfully.')
    @api.response(201, 'Review published successfully.')
    @api.response(300, 'invalid reviewed_course_id supplied')
    @api.response(404, 'Cant find course')
    def post(self, user):
        """Publish new review"""
        return save_new_review(user, request)


@api.route('/<int:review_id>')
@api.param('review_id', 'The Review identifier')
class GetReview(Resource):
    @login_required(api)
    @api.marshal_with(get_review_model(api), code=200, description='Review successfully retrieved')
    @api.response(404, 'Cant find review')
    @api.response(200, 'Review successfully retrieved')
    def get(self, user, review_id):
        """Get specific post"""
        return get_review_by_id(review_id)


@api.route('/<int:review_id>/comments')
@api.param('review_id', 'The Review identifier')
class GetReviewWithComments(Resource):
    @login_required(api)
    @api.marshal_with(get_review_with_comments_model(api), code=200, description='Review successfully retrieved')
    @api.response(404, 'Cant find review')
    @api.response(200, 'Review successfully retrieved')
    def get(self, user, review_id):
        """Get specific post, with comments"""
        return get_review_by_id(review_id)


@api.route('/<int:review_id>/like')
@api.param('review_id', 'The Review identifier')
class LikePost(Resource):
    @login_required(api)
    @api.marshal_with(get_like_dislike_score_model(api))
    @api.response(404, 'Cant find review')
    @api.response(210, 'liked review')
    @api.response(211, 'removed like from review')
    @api.response(212, 'removed dislike and liked review')
    def post(self, user, review_id):
        """Express like to specific post"""
        return like_review_by_id(user, review_id)


@api.route('/<int:review_id>/dislike')
@api.param('review_id', 'The Review identifier')
class DislikePost(Resource):
    @login_required(api)
    @api.marshal_with(get_like_dislike_score_model(api))
    @api.response(404, 'Cant find review')
    @api.response(210, 'liked review')
    @api.response(211, 'removed like from review')
    @api.response(212, 'removed dislike and liked review')
    def post(self, user, review_id):
        """Express dislike to specific post"""
        return dislike_review_by_id(user, review_id)
