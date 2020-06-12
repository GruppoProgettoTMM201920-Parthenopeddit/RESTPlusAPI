from app.main.model.post import Post
from app.main.model.user import User
from app.main.util.extract_resource import extract_resource
from app.main import db
from app.main.model.comment import Comment
from app.main.model.review import Review
from app.main.namespaces.pagination_decorator import get_paginated_result


def search_user(user, searched_user_id):
    if len(searched_user_id) < 3:
        response_object = {
            'status': 'error',
            'message': 'search string is too small. need 3 characters minimum',
        }
        return response_object, 300

    return User.query.whooshee_search(searched_user_id).limit(20).all(), 200


def change_display_name(user, request):
    try:
        new_name = extract_resource(request, 'display_name')
    except:
        return {}, 400

    user.display_name = new_name
    db.session.commit()

    return user, 201


def get_user_data(user, fetched_user_id):
    if fetched_user_id != user.id:
        fetched_user = User.query.filter(User.id == fetched_user_id).first_or_404()
    else:
        fetched_user = user

    return fetched_user, 200


def get_user_posts(user, fetched_user_id, page, per_page, request):
    try:
        timestamp = request.headers['transaction_start_datetime']
    except:
        timestamp = None

    if fetched_user_id != user.id:
        fetched_user = User.query.filter(User.id == fetched_user_id).first_or_404()
    else:
        fetched_user = user

    query = fetched_user.published_posts.order_by(
        Post.timestamp.desc()
    )

    return get_paginated_result(
        query=query,
        page=page,
        per_page=per_page,
        field=Post.timestamp,
        timestamp=timestamp
    )


def get_user_reviews(user, fetched_user_id, page, per_page, request):
    try:
        timestamp = request.headers['transaction_start_datetime']
    except:
        timestamp = None

    if fetched_user_id != user.id:
        fetched_user = User.query.filter(User.id == fetched_user_id).first_or_404()
    else:
        fetched_user = user

    query = fetched_user.published_reviews.order_by(
        Review.timestamp.desc()
    )

    return get_paginated_result(
        query=query,
        page=page,
        per_page=per_page,
        field=Review.timestamp,
        timestamp=timestamp
    )


def get_user_comments(user, fetched_user_id, page, per_page, request):
    try:
        timestamp = request.headers['transaction_start_datetime']
    except:
        timestamp = None

    if fetched_user_id != user.id:
        fetched_user = User.query.filter(User.id == fetched_user_id).first_or_404()
    else:
        fetched_user = user

    query = fetched_user.published_comments.order_by(
        Comment.timestamp.desc()
    )

    return get_paginated_result(
        query=query,
        page=page,
        per_page=per_page,
        field=Comment.timestamp,
        timestamp=timestamp
    )


def get_user_feed(user, page, per_page, request):
    try:
        timestamp = request.headers['transaction_start_datetime']
    except:
        timestamp = None

    query = user.get_posts_feed.order_by(
        Post.timestamp.desc()
    )

    return get_paginated_result(
        query=query,
        page=page,
        per_page=per_page,
        field=Post.timestamp,
        timestamp=timestamp
    )
