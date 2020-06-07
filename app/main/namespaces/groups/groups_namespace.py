from flask import request
from flask_restplus import Namespace, Resource

from app.main.namespaces.groups.group_decorator import require_group_membership, require_group_ownership
from app.main.namespaces.groups.groups_services import get_user_groups, create_group, get_user_group_invites, \
    get_group_by_id, leave_group, invite_member, answer_to_invite, get_group_invites, get_group_members, make_owner, \
    get_group_posts, publish_post_to_group
from app.main.namespaces.models_definition import get_user_group_model, get_new_group_model, \
    get_group_invite_model, get_group_model, get_users_id_list, get_answer_model, get_post_model, get_new_post_model
from app.main.util.auth_decorator import login_required
from main.util.selective_marshal_model_decorator import selective_marshal_with

api = Namespace('Groups', description="Users ad-hoc Groups framework")


@api.route("/")
class Groups(Resource):
    @login_required(api)
    @api.marshal_list_with(get_user_group_model(api), code=200, description="Successfully retrieved user groups")
    @api.response(200, "Successuflly retreived user groups")
    def get(self, user):
        """Get user joined groups"""
        return get_user_groups(user)

    @login_required(api)
    #@api.marshal_list_with(get_group_model(api), code=201, description='Successfully created group')
    #@api.marshal_list_with(get_group_invite_model(api), code=202, description='Successfully created group, and invited members')
    @selective_marshal_with([
        {
            'model': get_group_model(api),
            'code': 201,
            'list': False
        }, {
            'model': get_group_invite_model(api),
            'code': 202,
            'list': False
        }
    ])
    @api.expect(get_new_group_model(api))
    @api.response(300, 'Invalid payload. group name needed.')
    @api.response(201, 'Successfully created group', model=get_group_model(api))
    @api.response(202, 'Successfully created group, and invited members', model=get_group_invite_model(api))
    def post(self, user):
        """Create new group"""
        return create_group(user, request)


@api.route("/invites")
class UserGroupInvites(Resource):
    @login_required(api)
    @api.marshal_list_with(get_group_invite_model(api), code=200, description='Successfully retrieved user invites to group')
    @api.response(200, 'Successfully retreived user invites to group')
    def get(self, user):
        """Get user group invites"""
        return get_user_group_invites(user)


@api.route("/<int:group_id>")
@api.param('group_id', 'The Group identifier')
class GroupByID(Resource):
    @login_required(api)
    @require_group_membership(api)
    @api.marshal_with(get_group_model(api), code=200, description='Successfully retrieved group')
    @api.response(200, 'Successfully retrieved group')
    def get(self, group, **kwargs):
        """Get specific group info"""
        return get_group_by_id(group)


@api.route("/<int:group_id>/leave")
@api.param('group_id', 'The Group identifier')
class GroupLeave(Resource):
    @login_required(api)
    @require_group_membership(api)
    @api.response(201, 'Successfully left group')
    @api.response(202, 'Successfully left group. Group had no owner hence a new one was promoted')
    @api.response(203, 'Successfully left group. Group was empty hence disbanded')
    def post(self, user, group, **kwargs):
        """Leave a group"""
        return leave_group(user, group)


@api.route("/<int:group_id>/invite")
@api.param('group_id', 'The Group identifier')
class GroupInvite(Resource):
    @login_required(api)
    @require_group_ownership(api)
    @api.marshal_list_with(get_group_invite_model(api), code=201, description='Successfully invited user/s to group')
    @api.response(201, 'Successfully invited user/s to group')
    @api.expect(get_users_id_list(api))
    def post(self, user, group, **kwargs):
        """Invite users as group members"""
        return invite_member(user, group, request)

    @login_required(api)
    @require_group_membership(api)
    @api.marshal_list_with(get_group_invite_model(api), code=200, description="Successfully retrieved group'd invites")
    @api.response(200, "Successfully retrieved group'd invites")
    def get(self, group, **kwargs):
        """Get group invites"""
        return get_group_invites(group)


@api.route("/<int:group_id>/invite/answer")
@api.param('group_id', 'The Group identifier')
class GroupInviteAnswer(Resource):
    @login_required(api)
    @api.marshal_with(get_user_group_model(api), code=201, description='Successfully accepted invite to group')
    @api.expect(get_answer_model(api))
    @api.response(404, 'Group invite not found')
    @api.response(201, 'Successfully accepted invite to group')
    @api.response(202, 'Successfully declined invite')
    def post(self, user, group_id):
        """Accept or refuse a group invite"""
        return answer_to_invite(user, group_id, request)


@api.route("/<int:group_id>/members")
@api.param('group_id', 'The Group identifier')
class GroupMembers(Resource):
    @login_required(api)
    @require_group_membership(api)
    @api.marshal_list_with(get_user_group_model(api), code=200, description='Successfully retrieved group members info')
    @api.response(200, 'Successfully retrieved group members info')
    def get(self, group, **kwargs):
        """Get group's members list"""
        return get_group_members(group)


@api.route("/<int:group_id>/members/make_owner")
@api.param('group_id', 'The Group identifier')
class GroupsMembersMakeOnwer(Resource):
    @login_required(api)
    @require_group_ownership(api)
    @api.marshal_list_with(get_user_group_model(api), code=200, description='Successfully promoted user/s to owner')
    @api.response(200, 'Successfully promoted user/s to owner')
    @api.expect(get_users_id_list(api))
    def post(self, group, **kwargs):
        """Make a group member an owner"""
        return make_owner(group, request)


@api.route("/<int:group_id>/posts/", defaults={'per_page': 20, 'page': 1})
@api.route("/<int:group_id>/posts/<int:page>", defaults={'per_page': 20})
@api.route("/<int:group_id>/posts/<int:per_page>/<int:page>")
@api.param('page', 'Page to fetch')
@api.param('per_page', 'How many posts per page')
@api.param('group_id', 'The Group identifier')
class GroupPostsByPage(Resource):
    @login_required(api)
    @require_group_membership(api)
    @api.marshal_with(get_post_model(api), code=200, description='Post successfully retrieved')
    def get(self, group, per_page, page, **kwargs):
        """Get group published posts"""
        return get_group_posts(group, per_page, page)


@api.route("/<int:group_id>/posts")
@api.param('group_id', 'The Group identifier')
class NewGroupPost(Resource):
    @login_required(api)
    @require_group_membership(api)
    @api.expect(get_new_post_model(api))
    @api.marshal_with(get_post_model(api), code=201, description='Post published successfully.')
    def post(self, user, group, **kwargs):
        """Publish a post to the group's board"""
        return publish_post_to_group(user, group, request)


# @api.route("/<int:group_id>/messages")
# @api.param('group_id', 'The Group identifier')
# class GroupMessages(Resource):
#     @login_required(api)
#     @require_group_membership(api)
#     @api.marshal_list_with(get_message_model(api), code=200, description='Successfully retrieved messages')
#     def get(self, group, **kwargs):
#         """Get messages of the group-chat"""
#         return get_group_messages(group)
#
#     @login_required(api)
#     @require_group_membership(api)
#     @api.marshal_with(get_message_model(api), code=201, description='Message published successfully.')
#     @api.expect(get_new_message_model(api))
#     def post(self, user, group, **kwargs):
#         """Send a message to the group-chat"""
#         return send_message(user, group, request)
