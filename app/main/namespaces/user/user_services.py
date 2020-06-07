from app.main.model.post import Post
from app.main.model.user import User


def get_user_data(user, fetched_user_id):
    if fetched_user_id != user.id:
        fetched_user = User.query.filter(User.id == fetched_user_id).first_or_404()
    else:
        fetched_user = user

    return fetched_user, 200


def get_user_posts(user, fetched_user_id, per_page, page):
    if fetched_user_id != user.id:
        fetched_user = User.query.filter(User.id == fetched_user_id).first_or_404()
    else:
        fetched_user = user

    return fetched_user.published_posts.order_by(
        Post.timestamp.desc()
    ).paginate(
        per_page=per_page,
        page=page
    ).items, 200


def get_user_reviews(user, fetched_user_id, per_page, page):
    if fetched_user_id != user.id:
        fetched_user = User.query.filter(User.id == fetched_user_id).first_or_404()
    else:
        fetched_user = user

    return fetched_user.published_reviews.order_by(
        Post.timestamp.desc()
    ).paginate(
        per_page=per_page,
        page=page
    ).items, 200


def get_user_comments(user, fetched_user_id, per_page, page):
    if fetched_user_id != user.id:
        fetched_user = User.query.filter(User.id == fetched_user_id).first_or_404()
    else:
        fetched_user = user

    return fetched_user.published_comments.order_by(
        Post.timestamp.desc()
    ).paginate(
        per_page=per_page,
        page=page
    ).items, 200


def get_user_feed(user, per_page, page):
    return user.get_posts_feed.order_by(
        Post.timestamp.desc()
    ).paginate(
        per_page=per_page,
        page=page
    ).items, 200
