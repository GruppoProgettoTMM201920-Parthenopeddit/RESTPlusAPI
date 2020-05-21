from app.main.model.user import User


def get_user_data(user, fetched_user_id):
    if fetched_user_id is None:
        fetched_user_id = user.id
    fetched_user = User.query.filter(User.id == fetched_user_id).first_or_404()
    return fetched_user, 200


def get_user_feed(user, per_page, page):
    return user.get_posts_feed().paginate(per_page=per_page, page=page).items, 200
