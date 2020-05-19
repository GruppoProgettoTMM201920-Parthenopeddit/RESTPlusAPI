from app.main import db
from app.main.model.comment import Comment
from app.main.namespaces.content_accessibility import is_comment_accessible, is_content_accessible
from app.main.namespaces.like_dislike_framework import like_content, dislike_content


def save_new_comment(token, user_id, payload):
    commented_content_id = payload['commented_content_id']
    if commented_content_id is None:
        response_object = {
            'status': 'error',
            'message': 'no commented_content_id supplied',
        }
        return response_object, 300

    accessible, user, content = is_content_accessible(user_id, commented_content_id)

    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Trying to comment private post",
        }
        return response_object, 401

    root_content = content if content.type != 'comment' else content.root_content

    body = payload['body']
    new_comment = Comment(author=user, body=body, commented_content=content, root_content=root_content)
    db.session.add(new_comment)
    db.session.commit()

    response_object = {
        'status': 'success',
        'message': 'Comment published successfully',
        'id': new_comment.id
    }
    return response_object, 200


def get_comment_by_id(token, user_id, comment_id):
    accessible, user, comment = is_comment_accessible(user_id, comment_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Commented post is private",
        }
        return response_object, 401

    return comment, 200


def like_comment_by_id(token, user_id, comment_id):
    accessible, user, comment = is_comment_accessible(user_id, comment_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Commented post is private",
        }
        return response_object, 401

    return like_content(user, comment)


def dislike_comment_by_id(token, user_id, comment_id):
    accessible, user, comment = is_comment_accessible(user_id, comment_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Commented post is private",
        }
        return response_object, 401

    return dislike_content(user, comment)
