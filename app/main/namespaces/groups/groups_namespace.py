from flask import request
from flask_restplus import Namespace, Resource, fields

from app.main.util.auth_decorator import login_required
from app.main.namespaces.groups.groups_services import get_user_groups, create_group, get_user_group_invites, \
    get_group_by_id, leave_group
from app.main.namespaces.models_definition import get_user_group_model, get_new_group_model, get_simple_user_model, \
    get_group_invite_model, get_group_model

api = Namespace('Groups', description="Users ad-hoc Groups framework")


@api.route("/")
class Groups(Resource):
    @login_required(api)
    @api.marshal_list_with(get_user_group_model(api))
    @api.response(200, "Successuflly retreived user groups")
    def get(self, user):
        """Get user joined groups"""
        return get_user_groups(user)

    @login_required(api)
    @api.marshal_list_with(get_simple_user_model(api))
    @api.expect(get_new_group_model(api), validate=True)
    def post(self, user):
        """Create new group"""
        payload = request.json
        return create_group(user, payload)


@api.route("/invites")
class UserGroupInvites(Resource):
    @login_required(api)
    @api.marshal_list_with(get_group_invite_model(api))
    def get(self, user):
        """Get user group invites"""
        return get_user_group_invites(user)


@api.route("/<int:group_id>")
@api.param('group_id', 'The Group identifier')
class GroupByID(Resource):
    @login_required(api)
    @api.marshal_with(get_group_model(api))
    def get(self, user, group_id):
        """Get specific group info"""
        return get_group_by_id(user, group_id)


@api.route("/<int:group_id>/leave")
@api.param('group_id', 'The Group identifier')
class GroupLeave(Resource):
    @login_required(api)
    def post(self, user, group_id):
        """Leave a group"""
        return leave_group(user, group_id)


# @api.route("/<int:group_id>/invite")
# @api.param('group_id', 'The Group identifier')
# class GroupInvite(Resource):
#     @login_required
#     def post(self, user, group_id):
#         """Invite user as group member"""
#         # TODO
#         #   GET invited_user_id in payload
#         payload = request.json
#         return invite_member(user, group_id, payload)
#
#
# @api.route("/<int:group_id>/invite/answer")
# @api.param('group_id', 'The Group identifier')
# class GroupInviteAnswer(Resource):
#     @login_required
#     def post(self, user, group_id):
#         """Accept or refuse a group invite"""
#         # TODO
#         #   GET answer in payload
#         payload = request.json
#         return answer_to_invite(user, group_id, payload)
#
#
# @api.route("/<int:group_id>/members")
# @api.param('group_id', 'The Group identifier')
# class GroupMembers(Resource):
#     @login_required
#     def get(self, user, group_id):
#         """Get group's members list"""
#         return get_group_members(user, group_id)
#
#
# @api.route("/<int:group_id>/members/make_owner")
# @api.param('group_id', 'The Group identifier')
# class GroupsMembersMakeOnwer(Resource):
#     @login_required
#     def post(self, user, group_id):
#         """Make a group member an owner"""
#         # TODO
#         #   GET promoted_user_id in payload
#         payload = request.json
#         return make_owner(user, group_id, payload)
#
#
# @api.route("/<int:group_id>/messages")
# @api.param('group_id', 'The Group identifier')
# class GroupMessages(Resource):
#     @login_required
#     def get(self, user, group_id):
#         """Get messages of the group-chat"""
#         return get_group_messages(user, group_id)
#
#     @login_required
#     def post(self, user, group_id):
#         """Send a message to the group-chat"""
#         # TODO
#         #   GET message from payload
#         payload = request.json
#         return send_message(user, group_id, payload)
#
#
# @api.route("/<int:group_id>/posts")
# @api.param('group_id', 'The Group identifier')
# class GroupPosts(Resource):
#     @login_required
#     def get(self, user, group_id):
#         """Get group published posts"""
#         return get_group_posts(user, group_id)
#
#     @login_required
#     def post(self, user, group_id):
#         """Publish a post to the group's board"""
#         # TODO
#         #   GET post from payload
#         payload = request.json
#         return publish_post(user, group_id, payload)
#