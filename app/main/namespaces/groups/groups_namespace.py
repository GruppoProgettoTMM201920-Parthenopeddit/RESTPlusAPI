from flask import request
from flask_restplus import Namespace, Resource

from app.main.util.auth_decorator import login_required

api = Namespace('Groups', description="Users ad-hoc Groups framework")


@api.route("/")
class Groups(Resource):
    @login_required(api)
    def get(self, user):
        """Get user joined groups"""
        return get_user_groups(user)

    @login_required
    def post(self, user):
        """Create new group"""
        # TODO
        #   GET group data from payload
        payload = request.json
        return create_group(user, payload)


@api.route("/<int:group_id>")
@api.param('group_id', 'The Group identifier')
class GroupByID(Resource):
    @login_required
    def get(self, user, group_id):
        """Get specific group info"""
        return get_group_by_id(user, group_id)


@api.route("/<int:group_id>/leave")
@api.param('group_id', 'The Group identifier')
class GroupLeave(Resource):
    @login_required
    def post(self, user, group_id):
        """Leave a group"""
        return leave_group(user, group_id)


@api.route("/<int:group_id>/invite")
@api.param('group_id', 'The Group identifier')
class GroupInvite(Resource):
    @login_required
    def post(self, user, group_id):
        """Invite user as group member"""
        # TODO
        #   GET invited_user_id in payload
        payload = request.json
        return invite_member(user, group_id, payload)


@api.route("/<int:group_id>/invite/answer")
@api.param('group_id', 'The Group identifier')
class GroupInviteAnswer(Resource):
    @login_required
    def post(self, user, group_id):
        """Accept or refuse a group invite"""
        # TODO
        #   GET answer in payload
        payload = request.json
        return answer_to_invite(user, group_id, payload)


@api.route("/<int:group_id>/members")
@api.param('group_id', 'The Group identifier')
class GroupMembers(Resource):
    @login_required
    def get(self, user, group_id):
        """Get group's members list"""
        return get_group_members(user, group_id)


@api.route("/<int:group_id>/members/make_owner")
@api.param('group_id', 'The Group identifier')
class GroupsMembersMakeOnwer(Resource):
    @login_required
    def post(self, user, group_id):
        """Make a group member an owner"""
        # TODO
        #   GET promoted_user_id in payload
        payload = request.json
        return make_owner(user, group_id, payload)


@api.route("/<int:group_id>/messages")
@api.param('group_id', 'The Group identifier')
class GroupMessages(Resource):
    @login_required
    def get(self, user, group_id):
        """Get messages of the group-chat"""
        return get_group_messages(user, group_id)

    @login_required
    def post(self, user, group_id):
        """Send a message to the group-chat"""
        # TODO
        #   GET message from payload
        payload = request.json
        return send_message(user, group_id, payload)


@api.route("/<int:group_id>/posts")
@api.param('group_id', 'The Group identifier')
class GroupPosts(Resource):
    @login_required
    def get(self, user, group_id):
        """Get group published posts"""
        return get_group_posts(user, group_id)

    @login_required
    def post(self, user, group_id):
        """Publish a post to the group's board"""
        # TODO
        #   GET post from payload
        payload = request.json
        return publish_post(user, group_id, payload)
