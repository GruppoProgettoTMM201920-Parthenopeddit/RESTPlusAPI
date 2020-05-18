from app.main.model.user import User


def get_user_data(token, user_id, fetched_user_id):
    if fetched_user_id is None:
        fetched_user_id = user_id

    user = User.query.filter(User.id == fetched_user_id).first_or_404()

    return user, 200


def get_user_feed(token, user_id, per_page, page):
    user = User.query.filter(User.id == user_id).first_or_404()
    return user.get_posts_feed().paginate(per_page=per_page, page=page).items, 200
