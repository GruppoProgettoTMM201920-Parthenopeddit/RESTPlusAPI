from app.main import db
from app.main.model.comment import Comment
from app.main.namespaces.content_accessibility import is_comment_accessible, is_content_accessible
from app.main.namespaces.like_dislike_framework import like_content, dislike_content
from app.main.util.extract_resource import extract_resource


def save_new_comment(user, request):
    try:
        body = extract_resource(request, 'body')
    except:
        return {
            'status': 'error',
            'message': 'Missing expected data: Comment body'
        }, 452
    try:
        commented_content_id = int(extract_resource(request, 'commented_content_id'))
    except:
        return {
            'status': 'error',
            'message': 'Missing expected data: Comment commented-content id'
        }, 452

    accessible, content = is_content_accessible(user, commented_content_id)

    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Commented post is private',
        }
        return response_object, 401

    root_content = content if content.type != 'comment' else content.root_content

    new_comment = Comment(author=user, body=body, commented_content=content, root_content=root_content)
    db.session.add(new_comment)
    db.session.commit()

    return new_comment, 201


def get_comment_by_id(user, comment_id):
    accessible, comment = is_comment_accessible(user, comment_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Commented post is private',
        }
        return response_object, 401

    return comment, 200


def like_comment_by_id(user, comment_id):
    accessible, comment = is_comment_accessible(user, comment_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Commented post is private',
        }
        return response_object, 401

    return like_content(user, comment)


def dislike_comment_by_id(user, comment_id):
    accessible, comment = is_comment_accessible(user, comment_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': 'Commented post is private',
        }
        return response_object, 401

    return dislike_content(user, comment)
