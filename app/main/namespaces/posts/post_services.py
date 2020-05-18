from app.main import db
from app.main.model.board import Board
from app.main.model.post import Post
from app.main.model.user import User


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
    save_changes(new_post)

    response_object = {
        'status': 'success',
        'message': 'Post published successfully',
        'id': new_post.id
    }
    return response_object, 200


def get_post_by_id(token, user_id, post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    user = User.query.filter(User.id == user_id).first_or_404()

    if post.posted_to_board_id is not None:
        if post.posted_to_board not in user.boards.all():
            response_object = {
                'status': 'error',
                'message': "Post is private",
            }
            return response_object, 401

    return post, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()
