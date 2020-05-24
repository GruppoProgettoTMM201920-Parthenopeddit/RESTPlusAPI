from app.main.model.group import Group


def get_group_accessibility(user, group_id):
    membership = user.groups.filter(Group.id == group_id).first()

    if membership:
        return True, membership.is_owner, membership.group
    else:
        return False, False, None
