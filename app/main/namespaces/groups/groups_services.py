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

    new_group = Group(name=name, chat=GroupChat())
    db.session.add(new_group)
    db.session.add(GroupMember(user=user, group=new_group, is_owner=True))

    db.session.commit()

    # TODO
    #   SEND ALL GROUP INVITES IN WORKER THREAD
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
    group = user.joined_groups.filter(Group.id == group_id).first_or_404()
    GroupMember.query.filter(GroupMember.group_id == group.id, GroupMember.user_id == user.id).delete()

    if group.members.count() == 0:
        # TODO
        #   DELETE GROUP IN WORKER THREAD TO KEEP API RESPONSIVE
        db.session.delete(group)

        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully left group. Group was empty hence disbanded',
        }
        return response_object, 203
    elif group.members.filter(GroupMember.is_owner).count() == 0:
        new_owner = group.members.order_by(GroupMember.join_date).first()
        new_owner.is_owner = True

        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully left group. Group had no owner hence a new one was promoted',
        }
        return response_object, 202

    response_object = {
        'status': 'success',
        'message': 'Successfully left group',
    }
    return response_object, 201
