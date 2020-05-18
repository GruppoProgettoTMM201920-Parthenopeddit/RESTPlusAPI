from app.main import db
from app.main.model.comment import Comment
from app.main.model.content import Content
from app.main.model.group import Group
from app.main.model.user import User
from app.main.namespaces.like_dislike_framework import like_content, dislike_content


def save_new_comment(token, user_id, payload):
    commented_content_id = payload['commented_content_id']
    if commented_content_id is None:
        response_object = {
            'status': 'error',
            'message': 'no commented_content_id supplied',
        }
        return response_object, 300

    content = Content.query.filter(Content.id == commented_content_id).first_or_404()
    if not content:
        response_object = {
            'status': 'error',
            'message': 'invalid commented_content_id supplied',
        }
        return response_object, 300

    author_id = user_id
    body = payload['body']
    new_comment = Comment(author_id=author_id, body=body, commented_content_id=commented_content_id)
    db.session.add(new_comment)
    db.session.commit()

    response_object = {
        'status': 'success',
        'message': 'Comment published successfully',
        'id': new_comment.id
    }
    return response_object, 200


def get_comment_by_id(token, user_id, comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()
    user = User.query.filter(User.id == user_id).first_or_404()
    commented_content = comment.commented_content
    if commented_content.type == 'post':
        post = commented_content
        if post.posted_to_board_id is not None:
            response_object = {
                'status': 'error',
                'message': "Post is private",
            }
            return response_object, 401

    return comment, 200


def __is_comment_accessible(user_id, comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()
    user = User.query.filter(User.id == user_id).first_or_404()

    content = comment
    while content.type == 'comment':
        content = comment.commented_content
    if content.type == 'post':
        post = content
        if post.posted_to_board_id is not None:
            board = post.posted_to_board
            if board.type == 'group':
                group = board
                if group != user.joined_groups.filter(Group.id == group.id).first():
                    return False, None, None

    return True, user, comment


def like_comment_by_id(token, user_id, comment_id):
    accessible, user, comment = __is_comment_accessible(user_id, comment_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Commented post is private",
        }
        return response_object, 401

    return like_content(user, comment)


def dislike_comment_by_id(token, user_id, comment_id):
    accessible, user, comment = __is_comment_accessible(user_id, comment_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Commented post is private",
        }
        return response_object, 401

    return dislike_content(user, comment)
