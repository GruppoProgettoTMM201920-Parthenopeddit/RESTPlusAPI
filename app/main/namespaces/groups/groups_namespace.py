from flask import request
from flask_restplus import Namespace, Resource

from app.main.util.auth_decorator import login_required
from app.main.namespaces.groups.groups_services import get_user_groups, create_group, get_user_group_invites, \
    get_group_by_id, leave_group, invite_member, answer_to_invite, get_group_invites, get_group_members, make_owner, \
    get_group_posts, publish_post_to_group, get_group_messages, send_message
from app.main.namespaces.models_definition import get_user_group_model, get_new_group_model, get_simple_user_model, \
    get_group_invite_model, get_group_model, get_users_id_list, get_answer_model, get_content_model, ContentType, \
    get_new_post_model, get_message_model, get_new_message_model
from main.namespaces.groups.group_decorator import require_group_membership, require_group_ownership

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
    @api.marshal_list_with(get_group_invite_model(api))
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
    @require_group_membership(api)
    @api.marshal_with(get_group_model(api))
    def get(self, group, **kwargs):
        """Get specific group info"""
        return get_group_by_id(group)


@api.route("/<int:group_id>/leave")
@api.param('group_id', 'The Group identifier')
class GroupLeave(Resource):
    @login_required(api)
    @require_group_membership(api)
    def post(self, user, group, **kwargs):
        """Leave a group"""
        return leave_group(user, group)


@api.route("/<int:group_id>/invite")
@api.param('group_id', 'The Group identifier')
class GroupInvite(Resource):
    @login_required(api)
    @require_group_ownership(api)
    @api.marshal_list_with(get_group_invite_model(api))
    @api.expect(get_users_id_list(api))
    def post(self, user, group, **kwargs):
        """Invite user as group member"""
        payload = request.json
        return invite_member(user, group, payload)

    @login_required(api)
    @require_group_membership(api)
    @api.marshal_list_with(get_group_invite_model(api))
    def get(self, group, **kwargs):
        """Get group invites"""
        return get_group_invites(group)


@api.route("/<int:group_id>/invite/answer")
@api.param('group_id', 'The Group identifier')
class GroupInviteAnswer(Resource):
    @login_required(api)
    @api.marshal_with(get_user_group_model(api))
    @api.expect(get_answer_model(api), validate=True)
    def post(self, user, group_id):
        """Accept or refuse a group invite"""
        payload = request.json
        return answer_to_invite(user, group_id, payload)


@api.route("/<int:group_id>/members")
@api.param('group_id', 'The Group identifier')
class GroupMembers(Resource):
    @login_required(api)
    @require_group_membership(api)
    @api.marshal_list_with(get_user_group_model(api))
    def get(self, group, **kwargs):
        """Get group's members list"""
        return get_group_members(group)


@api.route("/<int:group_id>/members/make_owner")
@api.param('group_id', 'The Group identifier')
class GroupsMembersMakeOnwer(Resource):
    @login_required(api)
    @require_group_ownership(api)
    @api.marshal_list_with(get_user_group_model(api))
    @api.expect(get_users_id_list(api))
    def post(self, group, **kwargs):
        """Make a group member an owner"""
        payload = request.json
        return make_owner(group, payload)


@api.route("/<int:group_id>/posts")
@api.param('group_id', 'The Group identifier')
class GroupPosts(Resource):
    @login_required(api)
    @require_group_membership(api)
    @api.marshal_with(get_content_model(api, ContentType.POST), code=200, description='Post successfully retrieved')
    def get(self, group, **kwargs):
        """Get group published posts"""
        return get_group_posts(group)

    @login_required(api)
    @require_group_membership(api)
    @api.expect(get_new_post_model(api), validate=True)
    @api.marshal_with(get_content_model(api, ContentType.POST), code=201, description='Post published successfully.')
    def post(self, user, group, **kwargs):
        """Publish a post to the group's board"""
        payload = request.json
        return publish_post_to_group(user, group, payload)


@api.route("/<int:group_id>/messages")
@api.param('group_id', 'The Group identifier')
class GroupMessages(Resource):
    @login_required(api)
    @require_group_membership(api)
    @api.marshal_list_with(get_message_model(api))
    def get(self, group, **kwargs):
        """Get messages of the group-chat"""
        return get_group_messages(group)

    @login_required(api)
    @require_group_membership(api)
    @api.marshal_with(get_message_model(api))
    @api.expect(get_new_message_model(api))
    def post(self, user, group, **kwargs):
        """Send a message to the group-chat"""
        payload = request.json
        return send_message(user, group, payload)
