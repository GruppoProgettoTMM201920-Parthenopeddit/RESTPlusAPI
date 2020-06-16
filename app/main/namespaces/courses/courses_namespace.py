from flask import request
from flask_restplus import Namespace, Resource

from app.main.namespaces.courses.courses_services import search_course, get_user_courses, get_course_by_id, \
    follow_course, unfollow_course, get_course_posts, publish_post_to_course, get_course_followers, get_course_reviews, \
    publish_review_to_course
from app.main.namespaces.models_definition import get_course_model, get_post_model, get_new_post_model, \
    get_simple_user_model, get_review_model, get_new_review_model
from main.namespaces.auth.auth_decorator import login_required

api = Namespace('Courses', description="Uniparthenope courses framework")


@api.route("/search/<course_name>")
@api.param('course_name')
class CourseSearch(Resource):
    @login_required(api)
    @api.marshal_list_with(get_course_model(api))
    def get(self, course_name, **kwargs):
        return search_course(course_name)


@api.route("/")
class Courses(Resource):
    @login_required(api)
    @api.marshal_list_with(get_course_model(api))
    def get(self, user, **kwargs):
        return get_user_courses(user)


@api.route("/<int:course_id>")
@api.param('course_id')
class CourseByID(Resource):
    @login_required(api)
    @api.marshal_with(get_course_model(api))
    def get(self, course_id, **kwargs):
        return get_course_by_id(course_id)


@api.route("/<int:course_id>/followers")
@api.param('course_id')
class FollowCourse(Resource):
    @login_required(api)
    @api.marshal_list_with(get_simple_user_model(api))
    def get(self, course_id, **kwargs):
        return get_course_followers(course_id)


@api.route("/<int:course_id>/follow")
@api.param('course_id')
class FollowCourse(Resource):
    @login_required(api)
    def post(self, user, course_id):
        return follow_course(user, course_id)


@api.route("/<int:course_id>/unfollow")
@api.param('course_id')
class UnfollowCourseByID(Resource):
    @login_required(api)
    def post(self, user, course_id):
        return unfollow_course(user, course_id)


@api.route("/<int:course_id>/posts/<per_page>/<page>")
@api.param('page', 'Page to fetch')
@api.param('per_page', 'How many posts per page')
@api.param('course_id')
class CoursePostsByID(Resource):
    @login_required(api)
    @api.marshal_list_with(get_post_model(api), code=200, description='Post successfully retrieved')
    def get(self, course_id, per_page, page, **kwargs):
        return get_course_posts(course_id, per_page=int(per_page), page=int(page), request=request)


@api.route("/<int:course_id>/posts")
@api.param('course_id')
class NewCoursePost(Resource):
    @login_required(api)
    @api.expect(get_new_post_model(api))
    @api.marshal_with(get_post_model(api), code=201, description='Post published successfully.')
    def post(self, user, course_id, **kwargs):
        return publish_post_to_course(user, course_id, request)


@api.route("/<int:course_id>/reviews/<per_page>/<page>")
@api.param('page', 'Page to fetch')
@api.param('per_page', 'How many reviews per page')
@api.param('course_id')
class CourseReviewsByID(Resource):
    @login_required(api)
    @api.marshal_with(get_review_model(api), code=200, description='Review successfully retrieved')
    def get(self, course_id, per_page, page, **kwargs):
        return get_course_reviews(course_id, per_page=int(per_page), page=int(page), request=request)


@api.route("/<int:course_id>/reviews")
@api.param('course_id')
class NewCourseReview(Resource):
    @login_required(api)
    @api.expect(get_new_review_model(api))
    @api.marshal_with(get_review_model(api), code=201, description='Review published successfully.')
    def post(self, user, course_id, **kwargs):
        return publish_review_to_course(user, course_id, request)
