from app.main import db
from app.main.model.group import Group
from app.main.model.group_chat import GroupChat
from app.main.model.group_invite import GroupInvite
from app.main.model.group_member import GroupMember
from app.main.model.message import Message
from app.main.model.post import Post
from app.main.model.user import User
from app.main.util.extract_resource import extract_resource, extract_object_resource
from app.main.namespaces.pagination_decorator import get_paginated_result


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
        users_list = extract_object_resource(request, 'invited_members')

        # TODO
        #   SEND ALL GROUP INVITES IN WORKER THREAD
        invites = __send_group_invites(
            inviter_user=user,
            group=new_group,
            invited_users_id_list=users_list
        )

        if len(invites) > 0:
            db.session.add_all(invites)
            db.session.commit()

            return invites, 202
        else:
            raise Exception()
    except:
        print("exception raised")
        return new_group, 201


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
        users_list = extract_object_resource(request, 'users_list')
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

    return invites, 201


def undo_invite(group, other_user):
    invite = GroupInvite.query.filter(
        GroupInvite.group_id == group.id
    ).filter(
        GroupInvite.invited_id == other_user
    ).one()

    db.session.delete(invite)
    db.session.commit()

    return {}, 201


def kick_from_group(group, other_user):
    membership = GroupMember.query.filter(
        GroupMember.group_id == group.id
    ).filter(
        GroupMember.user_id == other_user
    ).filter(
        GroupMember.is_owner == False
    ).one()

    db.session.delete(membership)
    db.session.commit()

    return {}, 201


def get_group_invites(group):
    return group.invites.all(), 200


def search_user_for_group_invite(group, user_id):
    result = User.query.filter(
        User.id.notin_(group.involved_users.with_entities(User.id))
    ).whooshee_search(user_id).all()
    
    return result, 200


def answer_to_invite(user, group_id, request):
    try:
        accepted = bool(extract_resource(request, 'answer'))
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
        users_list = extract_object_resource(request, 'users_list')
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


def get_group_posts(group, per_page, page, request):
    try:
        timestamp = request.headers['transaction_start_datetime']
    except:
        timestamp = None

    query = group.posts.order_by(
        Post.timestamp.desc()
    )

    return get_paginated_result(
        query=query,
        page=page,
        per_page=per_page,
        field=Post.timestamp,
        timestamp=timestamp
    )


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
        replies_to_message_id = int(extract_resource(request, 'replies_to_message_id'))
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
#   MAKE NEXT METHODS CONCURRENT


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
            group.involved_users.with_entities(User.id)
        )
    ).all()

    invites = []
    for invited_user in invited_users:
        try:
            invites.append(GroupInvite(inviter=inviter_user, invited=invited_user, group=group))
        except:
            pass

    return invites
