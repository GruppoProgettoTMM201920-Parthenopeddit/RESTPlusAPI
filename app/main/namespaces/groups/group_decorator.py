from functools import wraps

from app.main.model.group_member import GroupMember


def check_group_accessibility(user, group_id):
    membership = user.groups.filter(GroupMember.group_id == group_id).first()

    if membership:
        return True, membership.is_owner, membership.group
    else:
        return False, False, None


def require_group_membership(api):
    def wrapper_func(f):
        @api.response(404, 'Group not found')
        @api.response(461, 'Group is private')
        @wraps(f)
        def decorated(*args, user, group_id, **kwargs):
            accessible, is_owner, group = check_group_accessibility(user, group_id)
            if not accessible:
                return {
                    'status': 'error',
                    'message': 'Group is private',
                }, 461
            return f(*args, **kwargs, user=user, group=group)

        return decorated

    return wrapper_func


def require_group_ownership(api):
    def wrapper_func(f):
        @api.response(404, 'Group not found')
        @api.response(461, 'Group is private')
        @api.response(462, 'Required group ownership')
        @wraps(f)
        def decorated(*args, user, group_id, **kwargs):
            accessible, is_owner, group = check_group_accessibility(user, group_id)
            if not accessible:
                return {
                    'status': 'error',
                    'message': 'Group is private',
                }, 461
            elif not is_owner:
                return {
                    'status': 'error',
                    'message': 'Group owneriship required',
                }, 462
            return f(*args, **kwargs, user=user, group=group)

        return decorated

    return wrapper_func
