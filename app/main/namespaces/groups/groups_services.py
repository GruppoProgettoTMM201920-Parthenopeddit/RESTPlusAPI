from app.main import db
from app.main.model.group import Group
from app.main.model.user import User
from app.main.model.group_invite import GroupInvite
from app.main.model.group_member import GroupMember
from app.main.model.group_chat import GroupChat


def get_user_groups(user):
    return user.groups.all(), 200


def create_group(user, payload):
    name = payload['group_name']
    if name is None or name == "":
        response_object = {
            'status': 'error',
            'message': 'Invalid payload. group name needed.',
        }
        return response_object, 300
    try:
        new_group = Group(name=name, chat=GroupChat())
        db.session.add(new_group)
        db.session.add(GroupMember(user=user, group=new_group, is_owner=True))

        users_id_list = []
        for user_id in payload['invited_members']:
            users_id_list.append(user_id)

        users = User.query.filter(User.id.in_(users_id_list)).all()

        invites = []
        invited_users = []
        for invited_user in users:
            invites.append(GroupInvite(inviter=user, invited=invited_user, group=new_group))
            invited_users.append(user)

        db.session.add_all(invites)
    except:
        response_object = {
            'status': 'error',
            'message': 'Internal server error.',
        }
        return response_object, 400

    db.session.commit()
    return invited_users, 201


def get_user_group_invites(user):
    return user.group_invites.all(), 200


def get_group_by_id(user, group_id):
    group = user.joined_groups.filter(Group.id == group_id).first()
    if group == None:
        response_object = {
            'status': 'error',
            'message': 'Group is private',
        }
        return response_object, 401
    return group, 200


def leave_group(user, group_id):
    # TODO
    return 200

