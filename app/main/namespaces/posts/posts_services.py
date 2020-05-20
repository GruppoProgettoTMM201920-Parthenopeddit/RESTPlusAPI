from app.main import db
from app.main.model.board import Board
from app.main.model.post import Post
from app.main.namespaces.content_accessibility import is_post_accessible
from app.main.namespaces.like_dislike_framework import like_content, dislike_content


def save_new_post(token, user_id, payload):
    board_id = payload['board_id']
    if board_id is not None:
        board = Board.query.filter(Board.id == board_id).first_or_404()
        if not board:
            response_object = {
                'status': 'error',
                'message': 'invalid board_id supplied',
            }
            return response_object, 300
    else:
        board_id = None

    author_id = user_id
    title = payload['title']
    body = payload['body']
    new_post = Post(author_id=author_id, title=title, body=body, posted_to_board_id=board_id)

    db.session.add(new_post)
    db.session.commit()

    return new_post, 200


def get_post_by_id(token, user_id, post_id):
    accessible, user, post = is_post_accessible(user_id, post_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Post is private",
        }
        return response_object, 401

    return post, 200


def like_post_by_id(token, user_id, post_id):
    accessible, user, post = is_post_accessible(user_id, post_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Post is private",
        }
        return response_object, 401

    return like_content(user, post)


def dislike_post_by_id(token, user_id, post_id):
    accessible, user, post = is_post_accessible(user_id, post_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Post is private",
        }
        return response_object, 401

    return dislike_content(user, post)
