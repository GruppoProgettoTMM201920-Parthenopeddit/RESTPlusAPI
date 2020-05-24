from app.main import db
from app.main.model.group import Group
from app.main.model.user import User
from app.main.model.group_invite import GroupInvite
from app.main.model.group_member import GroupMember
from app.main.model.group_chat import GroupChat
from app.main.namespaces.group_accessibility import get_user_group


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

    users_list = payload['invited_members']
    # TODO
    #   SEND ALL GROUP INVITES IN WORKER THREAD
    invites = __send_group_invites(
        inviter_user=user,
        group=new_group,
        invited_users_id_list=users_list
    )

    db.session.add_all(invites)
    db.session.commit()
    return invites, 201


def get_user_group_invites(user):
    return user.group_invites.all(), 200


def get_group_by_id(user, group_id):
    accessible, group = get_user_group(user, group_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Group is private',
        }
        return response_object, 401
    return group, 200


def leave_group(user, group_id):
    accessible, group = get_user_group(user, group_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Group is private',
        }
        return response_object, 401

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


def invite_member(user, group_id, payload):
    accessible, group = get_user_group(user, group_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Group is private',
        }
        return response_object, 401

    if not __is_user_owner(user, group):
        response_object = {
            'status': 'error',
            'message': 'Cant invite members if not owner',
        }
        return response_object, 480

    users_list = payload['users_list']
    # TODO
    #   SEND ALL GROUP INVITES IN WORKER THREAD
    invites = __send_group_invites(
        inviter_user=user,
        group=group,
        invited_users_id_list=users_list
    )

    db.session.add_all(invites)
    db.session.commit()
    return invites, 201


def get_group_invites(user, group_id):
    accessible, group = get_user_group(user, group_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Group is private',
        }
        return response_object, 401

    return group.invites.all(), 200


def __send_group_invites(inviter_user, group, invited_users_id_list):
    users = User.query.filter(User.id.in_(invited_users_id_list)).all()

    invites = []
    for invited_user in users:
        invites.append(GroupInvite(inviter=inviter_user, invited=invited_user, group=group))

    return invites


def __is_user_owner(user, group):
    return user.groups.filter(Group.id == group.id).first_or_404().is_owner


def answer_to_invite(user, group_id, payload):
    group_invite = user.group_invites.filter(GroupInvite.group_id == group_id).first_or_404()
    group = group_invite.group
    db.session.delete(group_invite)

    accepted = payload['answer']
    if accepted:
        membership = GroupMember(user=user, group=group, is_owner=False)
        db.session.add(membership)
        db.session.commit()
        return membership, 202
    else:
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully declined invite',
        }
        return response_object, 201


def get_group_members(user, group_id):
    accessible, group = get_user_group(user, group_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Group is private',
        }
        return response_object, 401

    return group.members.all(), 200


def make_owner(user, group_id, payload):
    accessible, group = get_user_group(user, group_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Group is private',
        }
        return response_object, 401

    if not __is_user_owner(user, group):
        response_object = {
            'status': 'error',
            'message': 'Cant invite members if not owner',
        }
        return response_object, 480

    users_list = payload['users_list']
    # TODO
    #   MAKE USERS OWNER IN WORKER THREAD
    owners = __make_owners(
        group=group,
        new_owners_id_list=users_list
    )

    db.session.commit()
    return owners, 201


def __make_owners(group, new_owners_id_list):
    members_to_make_owner = group.members.filter(GroupMember.is_owner == False, GroupMember.user_id.in_(new_owners_id_list)).all()

    new_owners = []
    for member in members_to_make_owner:
        member.is_owner = True
        new_owners.append(member)

    return new_owners
