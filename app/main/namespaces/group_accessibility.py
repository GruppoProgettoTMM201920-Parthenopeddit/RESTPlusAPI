from app.main.model.group import Group


def get_user_group(user, group_id):
    group = Group.query.filter(Group.id == group_id).first_or_404()

    if user.joined_groups.filter(Group.id == group_id).first() == group:
        return True, group
    else:
        return False, group
