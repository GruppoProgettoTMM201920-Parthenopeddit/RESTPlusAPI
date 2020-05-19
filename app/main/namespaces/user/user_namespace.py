from flask_restplus import Namespace, Resource

from app.main.namespaces.models_definition import get_complete_user_model, ContentType, get_content_model
from app.main.namespaces.user.user_services import get_user_data, get_user_feed
from app.main.util.auth_decorator import token_authenticated

api = Namespace('User', description="User's specific actions framework")


# TODO get full user info
#   get groups
#   get courses
#   get num likes
#   get num dislikes
#   get published content

@api.route("/", defaults={'fetched_user_id': None})
@api.route("/<string:fetched_user_id>", endpoint="/")
@api.param('fetched_user_id', 'ID of user to fetch')
class UserData(Resource):
    @token_authenticated
    @api.marshal_with(get_complete_user_model(api))
    def get(self, token, user_id, fetched_user_id):
        """Fetch user data"""
        return get_user_data(token, user_id, fetched_user_id)


@api.route("/feed/", defaults={'per_page': 20, 'page': 1})
@api.route("/feed/<int:page>", defaults={'per_page': 20})
@api.route("/feed/<int:per_page>/<int:page>")
@api.param('page', 'Page to fetch')
@api.param('per_page', 'How many posts per page')
class UserFeed(Resource):
    @token_authenticated
    @api.marshal_list_with(get_content_model(api, ContentType.POST))
    def get(self, token, user_id, per_page, page):
        """Fetch user posts feed"""
        return get_user_feed(token, user_id, per_page, page)

# TODO search users