import json

from app.main import db
from app.main.model.group import Group
from app.main.model.user import User
from app.main.model.group_invite import GroupInvite
from app.main.model.group_member import GroupMember
from app.main.model.group_chat import GroupChat
from app.main.model.post import Post
from app.main.model.message import Message
from app.main.util.extract_resource import extract_resource


def get_user_groups(user):
    return user.groups.all(), 200


def create_group(user, request):
    try:
        name = extract_resource(request, 'group_name')
    except:
        return {}, 400

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

    try:
        users_list = json.loads(extract_resource(request, 'invited_members'))

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
    except:
        return [], 201


def get_user_group_invites(user):
    return user.group_invites.all(), 200


def get_group_by_id(group):
    return group, 200


def leave_group(user, group):
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


def invite_member(user, group, request):
    try:
        users_list = json.loads(extract_resource(request, 'users_list'))
    except:
        return {}, 400

    # TODO
    #   SEND ALL GROUP INVITES IN WORKER THREAD
    invites = __send_group_invites(
        inviter_user=user,
        group=group,
        invited_users_id_list=users_list
    )

    db.session.add_all(invites)
    db.session.commit()

    print(invites)

    return invites, 201


def get_group_invites(group):
    return group.invites.all(), 200


def answer_to_invite(user, group_id, request):
    try:
        accepted = extract_resource(request, 'answer')
    except:
        return {}, 400

    group_invite = user.group_invites.filter(GroupInvite.group_id == group_id).first_or_404()
    group = group_invite.group
    db.session.delete(group_invite)

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


def get_group_members(group):
    return group.members.all(), 200


def make_owner(group, request):
    try:
        users_list = json.loads(extract_resource(request, 'users_list'))
    except:
        return {}, 400

    # TODO
    #   MAKE USERS OWNER IN WORKER THREAD
    owners = __make_owners(
        group=group,
        new_owners_id_list=users_list
    )

    db.session.commit()
    return owners, 201


def get_group_posts(group, per_page, page):
    # TODO Paginated results
    return group.posts.all(), 200


def publish_post_to_group(user, group, request):
    try:
        title = extract_resource(request, 'title')
        body = extract_resource(request, 'body')
    except:
        return {}, 400

    new_post = Post(author=user, title=title, body=body, posted_to_board=group)

    db.session.add(new_post)
    db.session.commit()

    return new_post, 201


def get_group_messages(group):
    return group.chat.received_messages.all(), 200


def send_message(user, group, request):
    try:
        message_text = extract_resource(request, 'body')
    except:
        return {}, 400

    try:
        replies_to_message_id = extract_resource(request, 'replies_to_message_id')
    except:
        replies_to_message_id = None

    new_message = Message(sender_user=user, receiver_chat=group.chat, body=message_text)

    if replies_to_message_id != None:
        try:
            replies_to_message = group.chat.received_messages.filter(Message.id == replies_to_message_id).first_or_404()
            new_message.replies_to_message = replies_to_message
        except:
            pass

    db.session.add(new_message)
    db.session.commit()
    return new_message, 201

# TODO
#   MAKE THIS SUBSEQUENT CONCURRENT


def __make_owners(group, new_owners_id_list):
    members_to_make_owner = group.members.filter(GroupMember.is_owner == False, GroupMember.user_id.in_(new_owners_id_list)).all()

    new_owners = []
    for member in members_to_make_owner:
        member.is_owner = True
        new_owners.append(member)

    return new_owners


def __send_group_invites(inviter_user, group, invited_users_id_list):
    invited_users = User.query.filter(
        User.id.in_(
            invited_users_id_list
        ),
        User.id.notin_(
            group.members.join(User).with_entities(User.id).union(
                group.invites.join(User, User.id == GroupInvite.invited_id).with_entities(User.id)
            )
        )
    ).all()

    invites = []
    for invited_user in invited_users:
        try:
            invites.append(GroupInvite(inviter=inviter_user, invited=invited_user, group=group))
        except:
            pass

    return invites
