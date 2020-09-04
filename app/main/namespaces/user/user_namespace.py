from flask import request
from flask_restplus import Namespace, Resource

from app.main.namespaces.models_definition import get_complete_user_model, get_post_model, get_review_model, \
    get_comment_model, get_simple_user_model, get_new_display_name_model
from app.main.namespaces.user.user_services import get_user_data, get_user_feed, get_user_posts, get_user_reviews, \
    get_user_comments, search_user, change_display_name
from app.main.namespaces.auth.auth_decorator import login_required

api = Namespace('User', description="User's specific actions framework")


@api.route("/search/<string:searched_user_id>")
@api.param('searched_user_id', 'ID of user to search')
class SearchUser(Resource):
    @login_required(api)
    @api.marshal_list_with(get_simple_user_model(api))
    def get(self, user, searched_user_id):
        """Search user by ID"""
        return search_user(user, searched_user_id)


@api.route("/display_name")
class SetDisplayName(Resource):
    @login_required(api)
    @api.expect(get_new_display_name_model(api))
    @api.marshal_with(get_simple_user_model(api))
    def post(self, user):
        """change user displayed name"""
        return change_display_name(user, request)


@api.route("/<string:fetched_user_id>")
@api.param('fetched_user_id', 'ID of user to fetch')
class UserData(Resource):
    @login_required(api)
    @api.marshal_with(get_complete_user_model(api))
    def get(self, user, fetched_user_id):
        """Fetch user data"""
        return get_user_data(user, fetched_user_id)


@api.route("/<string:fetched_user_id>/published_posts/<per_page>/<page>")
@api.param('page', 'Page to fetch')
@api.param('per_page', 'How many posts per page')
@api.param('fetched_user_id', 'ID of user to fetch')
class UserPosts(Resource):
    @login_required(api)
    @api.marshal_list_with(get_post_model(api))
    def get(self, user, fetched_user_id, per_page, page, **kwargs):
        """Fetch user published posts"""
        return get_user_posts(user, fetched_user_id, per_page=int(per_page), page=int(page), request=request)


@api.route("/<string:fetched_user_id>/published_reviews/<per_page>/<page>")
@api.param('page', 'Page to fetch')
@api.param('per_page', 'How many posts per page')
@api.param('fetched_user_id', 'ID of user to fetch')
class UserReviews(Resource):
    @login_required(api)
    @api.marshal_list_with(get_review_model(api))
    def get(self, user, fetched_user_id, per_page, page, **kwargs):
        """Fetch user published posts"""
        return get_user_reviews(user, fetched_user_id, per_page=int(per_page), page=int(page), request=request)


@api.route("/<string:fetched_user_id>/published_comments/<per_page>/<page>")
@api.param('page', 'Page to fetch')
@api.param('per_page', 'How many posts per page')
@api.param('fetched_user_id', 'ID of user to fetch')
class UserComments(Resource):
    @login_required(api)
    @api.marshal_list_with(get_comment_model(api))
    def get(self, user, fetched_user_id, per_page, page, **kwargs):
        """Fetch user published posts"""
        return get_user_comments(user, fetched_user_id, per_page=int(per_page), page=int(page), request=request)


@api.route("/feed/<per_page>/<page>")
@api.param('page', 'Page to fetch')
@api.param('per_page', 'How many posts per page')
class UserFeed(Resource):
    @login_required(api)
    @api.marshal_list_with(get_post_model(api))
    def get(self, user, per_page, page, **kwargs):
        """Fetch user posts feed"""
        return get_user_feed(user=user, per_page=int(per_page), page=int(page), request=request)
